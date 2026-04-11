from __future__ import annotations

import json
from pathlib import Path


APP_NAME = "Canada Tracker"
APP_SLUG = "canada-tracker"
DEFAULT_DB_DIR = Path.home() / ".local" / "share" / "canada-tracker"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "canada_tracker.db"
RUNTIME_CONFIG_PATH = Path.home() / ".config" / "canada-tracker" / "config.json"

DEFAULT_SETTINGS: dict[str, object] = {
    "financial_goal": 5000.0,
    "english_goal_minutes": 6000,
    "daily_water_goal": 1,
    "daily_training_goal": 1,
    "daily_food_goal": 1,
    "daily_sleep_goal": 1,
    "daily_work_goal": 1,
    "daily_cardio_goal": 1,
    "daily_mobility_goal": 1,
    "score_threshold_good": 80,
    "score_threshold_mid": 40,
    "weight_water": 15,
    "weight_food": 15,
    "weight_training": 15,
    "weight_english": 15,
    "weight_work": 20,
    "weight_sleep": 10,
    "weight_cardio": 5,
    "weight_mobility": 5,
    "accent_color": "#7cc7ff",
}

DEFAULT_RUNTIME_CONFIG: dict[str, object] = {
    "db_path": str(DEFAULT_DB_PATH),
}

BOOLEAN_FIELDS = {
    "water",
    "ate_well",
    "trained",
    "studied_english",
    "worked_progress",
    "slept_well",
    "cardio",
    "mobility",
}


def ensure_data_dir(path: str | Path | None = None) -> Path:
    db_path = Path(path) if path else DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def load_runtime_config() -> dict[str, object]:
    if not RUNTIME_CONFIG_PATH.exists():
        RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        save_runtime_config(DEFAULT_RUNTIME_CONFIG)
        return dict(DEFAULT_RUNTIME_CONFIG)
    return {**DEFAULT_RUNTIME_CONFIG, **json.loads(RUNTIME_CONFIG_PATH.read_text())}


def save_runtime_config(config: dict[str, object]) -> None:
    RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG_PATH.write_text(json.dumps(config, indent=2))


def encode_setting(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def parse_setting(raw: str, default: object) -> object:
    if isinstance(default, bool):
        return raw.lower() in {"1", "true", "yes", "on"}
    if isinstance(default, int):
        return int(float(raw))
    if isinstance(default, float):
        return float(raw)
    if isinstance(default, (dict, list)):
        return json.loads(raw)
    return raw
