from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, PositiveInt
from typing import List, Literal, Optional


__all__ = ["Character"]


class Character(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    name: str
    aliases: Optional[List[str]] = None
    faction_id: str
    gender: Literal["male", "female", "nonbinary", "unknown"]
    birth: PositiveInt
    death: Optional[PositiveInt] = None
    age: Optional[int] = None
    occupation: str
    personality: List[str]
    values: List[str]
    motives: List[str]
    skills: List[str]
    secrets: Optional[List[str]] = None
    appearance: str
    signature_items: Optional[List[str]] = None
    backstory: str = Field(..., min_length=120, max_length=220)
    relationship_seeds: Optional[List[str]] = None


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "characters.schema.json"
_schema_path.write_text(json.dumps(Character.model_json_schema(), indent=2))
