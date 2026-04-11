from __future__ import annotations

from datetime import date, datetime, timedelta


def calculate_daily_score(log: dict[str, object], settings: dict[str, object]) -> int:
    mapping = {
        "water": "weight_water",
        "ate_well": "weight_food",
        "trained": "weight_training",
        "studied_english": "weight_english",
        "worked_progress": "weight_work",
        "slept_well": "weight_sleep",
        "cardio": "weight_cardio",
        "mobility": "weight_mobility",
    }
    score = 0
    for field, weight_key in mapping.items():
        if int(log.get(field, 0) or 0):
            score += int(settings[weight_key])
    return max(0, min(100, score))


def classify_score(score: int, settings: dict[str, object]) -> str:
    good = int(settings["score_threshold_good"])
    mid = int(settings["score_threshold_mid"])
    if score >= good:
        return "good"
    if score >= mid:
        return "mid"
    return "low"


def current_streak(dates: list[str]) -> int:
    normalized = sorted({datetime.fromisoformat(item).date() for item in dates}, reverse=True)
    if not normalized:
        return 0
    streak = 0
    expected = normalized[0]
    if expected not in {date.today(), date.today() - timedelta(days=1)}:
        return 0
    for item in normalized:
        if item == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif item > expected:
            continue
        else:
            break
    return streak
