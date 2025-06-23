from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, conlist, confloat, PositiveInt
from typing import List, Literal, Optional

__all__ = ["Puzzle", "Event", "Events", "SceneType"]

SceneType = Literal[
    "dialogue",
    "investigation",
    "action",
    "cinematic",
    "flashback",
]


class Puzzle(BaseModel):
    id: str = Field(..., pattern=r"^PUZ-\d{3}$")
    puzzle_type: Literal["logic", "pattern", "riddle", "skill"]
    description: str
    solution: str
    reward_clue: Optional[str] = None


class Event(BaseModel):
    id: str = Field(..., pattern=r"^E-\d{2}-\d{2}$")
    beat_id: str
    order: PositiveInt
    scene_type: SceneType
    title: str
    synopsis: str = Field(..., min_length=40, max_length=120)
    location: str
    absolute_ts: Optional[str] = None
    characters: conlist(str, min_length=1)
    npcs: Optional[List[str]] = None
    player_role: Literal["direct_control", "observer", "flashback"]
    objective: str
    success_state: str
    failure_state: Optional[str] = None
    branching_tags: Optional[List[str]] = None
    clue_ids: Optional[List[str]] = None
    puzzle: Optional[Puzzle] = None
    ambience_notes: Optional[str] = None


class Events(BaseModel):
    events: List[Event]


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "events.schema.json"
_schema_path.write_text(json.dumps(Events.model_json_schema(), indent=2) + "\n")
