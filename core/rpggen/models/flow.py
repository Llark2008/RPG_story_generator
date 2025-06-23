from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, constr
from typing import Dict, List, Literal, Optional

__all__ = ["Condition", "Transition", "NarrativeFlow"]


class Condition(BaseModel):
    expression: str
    required_clues: Optional[List[str]] = None
    required_events: Optional[List[str]] = None


class Transition(BaseModel):
    id: constr(pattern=r"^TR-[0-9A-F]{8}$")
    from_event: str
    to_event: str
    condition: Optional[Condition] = None


class NarrativeFlow(BaseModel):
    flow_mode: Literal["linear", "branching-tree", "hub-spoke"]
    default_pov: Literal["single_character", "multi_character", "omniscient"]
    entry_event: str
    end_events: List[str]
    timeline_order: List[str]
    pov_map: Dict[str, str]
    transitions: List[Transition]


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "narrative_flow.schema.json"
_schema_path.write_text(json.dumps(NarrativeFlow.model_json_schema(), indent=2) + "\n")
