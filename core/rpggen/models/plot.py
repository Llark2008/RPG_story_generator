from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, conlist
from typing import List, Literal, Optional

__all__ = ["Beat", "PlotOutline", "ConflictType"]

ConflictType = Literal[
    "mystery",
    "investigation",
    "heist",
    "pursuit",
    "revelation",
    "confrontation",
    "escape",
    "betrayal",
]


class Beat(BaseModel):
    id: str = Field(..., pattern=r"^B\d{2}$")
    order: int
    title: str
    summary: str = Field(..., min_length=40, max_length=120)
    protagonists: conlist(str, min_length=1, max_length=3)
    antagonists: Optional[conlist(str, min_length=1, max_length=3)] = None
    location: Optional[str] = None
    timestamp: Optional[str] = None
    conflict_type: ConflictType
    stakes: str
    clue_introduced: Optional[List[str]] = None
    foreshadow: Optional[str] = None
    is_twist: bool
    tension_level: int = Field(..., ge=1, le=10)
    dependencies: Optional[List[str]] = None


class PlotOutline(BaseModel):
    theme: str
    structure_mode: Literal["three_act", "kishotenketsu", "linear"]
    beats: List[Beat]
    pacing_curve: Optional[List[int]] = None


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "plot_outline.schema.json"
_schema_path.write_text(json.dumps(PlotOutline.model_json_schema(), indent=2) + "\n")
