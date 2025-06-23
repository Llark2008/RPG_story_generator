from __future__ import annotations

from pathlib import Path
import json
from pydantic import BaseModel, Field, conlist
from typing import List, Literal, Optional

__all__ = [
    "DialogueLine",
    "PuzzleText",
    "ScriptMeta",
    "EventScript",
    "ScriptsPackage",
]


class DialogueLine(BaseModel):
    speaker_id: str
    text: str
    emotion: Optional[str] = ""
    branch_tag: Optional[str] = ""


class PuzzleText(BaseModel):
    puzzle_id: str = Field(..., pattern=r"^PUZ-\d{3}$")
    hint_success: str
    hint_failure: str
    reward_clue_copy: Optional[str] = None


class ScriptMeta(BaseModel):
    event_id: str
    lang: Literal["zh_CN", "en_US", "jp_JP"]
    pov: str
    scene_type: str
    branch_root: Optional[str] = None
    word_count_est: int


class EventScript(BaseModel):
    meta: ScriptMeta
    dialogues: conlist(DialogueLine, min_length=1)
    puzzle_text: Optional[PuzzleText] = None
    stage_notes: Optional[str] = None


class ScriptsPackage(BaseModel):
    scripts: List[EventScript]


_schema_dir = Path(__file__).resolve().parent
_schema_path = _schema_dir / "scripts.schema.json"
_schema_path.write_text(json.dumps(ScriptsPackage.model_json_schema(), indent=2))
