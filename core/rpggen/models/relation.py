from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, conlist, confloat
from typing import List, Literal, Optional


__all__ = ["Relation", "Relations", "RelationType"]

RelationType = Literal[
    "mentor",
    "rival",
    "ally",
    "family",
    "betrayal",
    "employer",
    "client",
    "unknown",
]


class Relation(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    source_id: str
    target_id: str
    type: RelationType
    direction: Literal["directed", "undirected"]
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    secrecy_level: Literal["public", "private", "secret"]
    confidence: confloat(ge=0, le=1)
    description: str = Field(..., min_length=60, max_length=120)
    evidence_seeds: Optional[conlist(str, max_length=4)] = None


class Relations(BaseModel):
    relations: List[Relation]


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "relations.schema.json"
_schema_path.write_text(json.dumps(Relations.model_json_schema(), indent=2))
