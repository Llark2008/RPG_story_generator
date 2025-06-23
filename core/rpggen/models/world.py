from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field
from typing import List, Literal, Optional


__all__ = [
    "Technology",
    "SpecialEnergy",
    "Faction",
    "HistoricalEvent",
    "NotableFigure",
    "ProperNoun",
    "World",
]


class Technology(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    name: str
    era: Literal["experimental", "early", "mature"]
    description: str = Field(..., min_length=40, max_length=180)


class SpecialEnergy(BaseModel):
    name: str
    discovery_year: int
    physical_form: Literal["plasma", "crystal", "field", "organism"]
    properties: List[str]
    hazards: List[str]
    applications: Optional[List[str]] = None
    description: str = Field(..., min_length=120)


class Faction(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    name: str
    motive: str
    doctrine: str
    status: Literal["active", "dormant", "destroyed"]
    founding_year: int
    description: str = Field(..., min_length=100)


class HistoricalEvent(BaseModel):
    year: int
    title: str
    description: str


class NotableFigure(BaseModel):
    name: str
    faction_id: Optional[str] = None
    role: str
    birth: int
    death: Optional[int] = None
    biography: str = Field(..., min_length=40)


class ProperNoun(BaseModel):
    name: str
    category: Literal[
        "technology",
        "energy",
        "faction",
        "location",
        "event",
        "project",
        "figure",
        "other",
    ]
    description: str = Field(..., min_length=40, max_length=100)


class World(BaseModel):
    setting: str
    global_theme: str
    technologies: List[Technology]
    special_energy: SpecialEnergy
    factions: List[Faction]
    historical_timeline: List[HistoricalEvent]
    notable_figures: List[NotableFigure]
    proper_nouns: List[ProperNoun]


# Auto export JSON schema for each primary model

_schema_dir = Path(__file__).resolve().parent

for model_cls, name in [
    (World, "world"),
    (Technology, "technology"),
    (SpecialEnergy, "special_energy"),
    (Faction, "faction"),
    (HistoricalEvent, "historical_event"),
    (NotableFigure, "notable_figure"),
    (ProperNoun, "proper_noun"),
]:
    schema_path = _schema_dir / f"{name}.schema.json"
    schema_path.write_text(
        json.dumps(model_cls.model_json_schema(), indent=2) + "\n"
    )
