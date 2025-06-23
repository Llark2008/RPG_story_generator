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
    "World",
]


class Technology(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    name: str
    era: Literal["experimental", "early", "mature"]
    description: str


class SpecialEnergy(BaseModel):
    name: str
    discovery_year: int
    physical_form: Literal["plasma", "crystal", "field", "organism"]
    properties: List[str]
    hazards: List[str]
    applications: Optional[List[str]] = None
    description: str


class Faction(BaseModel):
    id: str = Field(..., pattern="^[a-z0-9_]+$")
    name: str
    motive: str
    doctrine: str
    status: Literal["active", "dormant", "destroyed"]
    founding_year: int
    description: str


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
    biography: str


class World(BaseModel):
    setting: str
    global_theme: str
    technologies: List[Technology]
    special_energy: SpecialEnergy
    factions: List[Faction]
    historical_timeline: List[HistoricalEvent]
    notable_figures: List[NotableFigure]


# Auto export JSON schema for each primary model

_schema_dir = Path(__file__).resolve().parent

for model_cls, name in [
    (World, "world"),
    (Technology, "technology"),
    (SpecialEnergy, "special_energy"),
    (Faction, "faction"),
    (HistoricalEvent, "historical_event"),
    (NotableFigure, "notable_figure"),
]:
    schema_path = _schema_dir / f"{name}.schema.json"
    schema_path.write_text(
        json.dumps(model_cls.model_json_schema(), indent=2) + "\n"
    )
