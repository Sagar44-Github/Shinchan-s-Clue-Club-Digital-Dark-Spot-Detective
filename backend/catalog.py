from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).with_name("catalog.json")
CHALLENGE_PATH = Path(__file__).with_name("challenge_cases.json")


def all_cases() -> list[dict[str, Any]]:
    guided = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    challenges = json.loads(CHALLENGE_PATH.read_text(encoding="utf-8"))
    for item in guided:
        item.setdefault("play_mode", "guided")
    return challenges + guided


def find_case(slug: str) -> dict[str, Any] | None:
    return next((item for item in all_cases() if item["slug"] == slug), None)


def public_index() -> list[dict[str, Any]]:
    result = []
    for item in all_cases():
        result.append({key: item[key] for key in (
            "slug", "title", "category", "level", "description", "question", "context", "jurisdiction", "decision_date"
        )})
        result[-1]["play_mode"] = item.get("play_mode", "guided")
        challenge = item.get("challenge")
        if challenge:
            # The public sample library may show the challenge prompt, but all
            # solution assistance must be requested through the progressive
            # hint endpoint so players can inspect evidence first.
            result[-1]["challenge"] = {key: value for key, value in challenge.items() if key not in {"answer_id", "resolution", "hints", "hint"}}
        result[-1]["source_count"] = len(item["sources"])
        result[-1]["requirement_count"] = len(item["requirements"])
        result[-1]["sample_only"] = True
    return result
