from __future__ import annotations

from datetime import datetime

from canada_tracker.models.achievements import ACHIEVEMENTS, Achievement


class AchievementService:
    def __init__(self, database) -> None:
        self.database = database

    def definitions(self) -> list[Achievement]:
        return ACHIEVEMENTS

    def evaluate(self, metrics: dict[str, float]) -> list[str]:
        with self.database.connect() as conn:
            unlocked = {
                row["achievement_id"]
                for row in conn.execute("SELECT achievement_id FROM achievement_unlocks").fetchall()
            }
            newly_unlocked: list[str] = []
            now = datetime.now().isoformat(timespec="seconds")
            for achievement in ACHIEVEMENTS:
                if achievement.achievement_id in unlocked:
                    continue
                if float(metrics.get(achievement.metric, 0)) >= float(achievement.threshold):
                    conn.execute(
                        """
                        INSERT INTO achievement_unlocks(achievement_id, unlocked_at)
                        VALUES(?, ?)
                        """,
                        (achievement.achievement_id, now),
                    )
                    newly_unlocked.append(achievement.achievement_id)
        return newly_unlocked

    def all_with_status(self, metrics: dict[str, float]) -> list[dict[str, object]]:
        with self.database.connect() as conn:
            unlock_rows = conn.execute(
                "SELECT achievement_id, unlocked_at FROM achievement_unlocks"
            ).fetchall()
        unlocked = {row["achievement_id"]: row["unlocked_at"] for row in unlock_rows}
        items = []
        for achievement in ACHIEVEMENTS:
            current_value = float(metrics.get(achievement.metric, 0))
            progress = min(100.0, (current_value / float(achievement.threshold)) * 100) if achievement.threshold else 0.0
            items.append(
                {
                    "achievement_id": achievement.achievement_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "category": achievement.category,
                    "metric": achievement.metric,
                    "threshold": achievement.threshold,
                    "current_value": current_value,
                    "progress_percent": progress,
                    "unlocked": achievement.achievement_id in unlocked,
                    "unlocked_at": unlocked.get(achievement.achievement_id, ""),
                }
            )
        return items
