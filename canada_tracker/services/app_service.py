from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta

from canada_tracker.config import BOOLEAN_FIELDS, load_runtime_config, save_runtime_config
from canada_tracker.database import Database
from canada_tracker.services.achievement_service import AchievementService
from canada_tracker.services.scoring import calculate_daily_score, classify_score, current_streak


class AppService:
    def __init__(self, db_path: str | None = None) -> None:
        runtime = load_runtime_config()
        self.database = Database(db_path or str(runtime["db_path"]))
        self.database.record_launch()
        self.achievements = AchievementService(self.database)
        self.refresh_achievements()

    def get_settings(self) -> dict[str, object]:
        return self.database.get_settings()

    def save_settings(self, updates: dict[str, object]) -> bool:
        db_path = updates.pop("db_path", None)
        db_changed = False
        if db_path:
            db_changed = str(db_path) != str(self.database.db_path)
            save_runtime_config({"db_path": db_path})
        self.database.save_settings(updates)
        self.refresh_achievements()
        return db_changed

    def add_profit_entry(self, amount: float, source: str, entry_date: str, note: str) -> list[str]:
        with self.database.connect() as conn:
            conn.execute(
                """
                INSERT INTO profit_entries(amount, source, entry_date, note, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (amount, source.strip(), entry_date, note.strip(), datetime.now().isoformat(timespec="seconds")),
            )
        return self.refresh_achievements()

    def list_profit_entries(self) -> list[dict[str, object]]:
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, amount, source, entry_date, note
                FROM profit_entries
                ORDER BY entry_date DESC, id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def add_english_session(
        self, duration_minutes: int, study_type: str, session_date: str, note: str
    ) -> list[str]:
        with self.database.connect() as conn:
            conn.execute(
                """
                INSERT INTO english_sessions(duration_minutes, study_type, session_date, note, created_at)
                VALUES(?, ?, ?, ?, ?)
                """,
                (
                    duration_minutes,
                    study_type.strip(),
                    session_date,
                    note.strip(),
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
        return self.refresh_achievements()

    def list_english_sessions(self) -> list[dict[str, object]]:
        with self.database.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, duration_minutes, study_type, session_date, note
                FROM english_sessions
                ORDER BY session_date DESC, id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def save_daily_log(self, payload: dict[str, object]) -> list[str]:
        now = datetime.now().isoformat(timespec="seconds")
        fields = [
            "log_date",
            "water",
            "ate_well",
            "trained",
            "studied_english",
            "worked_progress",
            "slept_well",
            "cardio",
            "mobility",
            "mood",
            "weight",
            "note",
        ]
        values = [payload.get(field) for field in fields]
        with self.database.connect() as conn:
            conn.execute(
                """
                INSERT INTO daily_logs(
                    log_date, water, ate_well, trained, studied_english, worked_progress,
                    slept_well, cardio, mobility, mood, weight, note, created_at, updated_at
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(log_date) DO UPDATE SET
                    water = excluded.water,
                    ate_well = excluded.ate_well,
                    trained = excluded.trained,
                    studied_english = excluded.studied_english,
                    worked_progress = excluded.worked_progress,
                    slept_well = excluded.slept_well,
                    cardio = excluded.cardio,
                    mobility = excluded.mobility,
                    mood = excluded.mood,
                    weight = excluded.weight,
                    note = excluded.note,
                    updated_at = excluded.updated_at
                """,
                (*values, now, now),
            )
        return self.refresh_achievements()

    def get_daily_log(self, log_date: str) -> dict[str, object] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT * FROM daily_logs WHERE log_date = ?",
                (log_date,),
            ).fetchone()
        return dict(row) if row else None

    def list_daily_logs(self) -> list[dict[str, object]]:
        with self.database.connect() as conn:
            rows = conn.execute("SELECT * FROM daily_logs ORDER BY log_date DESC").fetchall()
        return [dict(row) for row in rows]

    def metrics(self) -> dict[str, object]:
        settings = self.get_settings()
        profits = self.list_profit_entries()
        sessions = self.list_english_sessions()
        logs = self.list_daily_logs()
        profit_total = round(sum(float(row["amount"]) for row in profits), 2)
        english_minutes = sum(int(row["duration_minutes"]) for row in sessions)
        english_dates = sorted({row["session_date"] for row in sessions})
        studied_streak = current_streak(english_dates)
        enriched_logs = [self._enrich_log(log, settings) for log in logs]
        good_dates = [log["log_date"] for log in enriched_logs if log["classification"] == "good"]
        perfect_days = sum(1 for log in enriched_logs if log["score"] == 100)
        weekly_logs = [log for log in enriched_logs if log["log_date"] >= (date.today() - timedelta(days=6)).isoformat()]
        monthly_logs = [log for log in enriched_logs if log["log_date"] >= (date.today() - timedelta(days=29)).isoformat()]
        average_daily = round(
            sum(log["score"] for log in weekly_logs) / len(weekly_logs), 1
        ) if weekly_logs else 0.0
        classification_counts = Counter(log["classification"] for log in enriched_logs)
        weekly_habit_totals = {
            field: sum(int(log.get(field, 0) or 0) for log in weekly_logs)
            for field in BOOLEAN_FIELDS
        }
        financial_goal = float(settings["financial_goal"])
        english_goal = int(settings["english_goal_minutes"])
        financial_progress = round((profit_total / financial_goal) * 100, 1) if financial_goal else 0.0
        english_progress = round((english_minutes / english_goal) * 100, 1) if english_goal else 0.0
        goal_progress = round((financial_progress + english_progress) / 2, 1)
        today_log = next((log for log in enriched_logs if log["log_date"] == date.today().isoformat()), None)
        recent_activity = self._recent_activity(profits, sessions, enriched_logs)
        with self.database.connect() as conn:
            launch_count = conn.execute("SELECT COUNT(*) AS total FROM app_launches").fetchone()["total"]
            unlocked_count = conn.execute("SELECT COUNT(*) AS total FROM achievement_unlocks").fetchone()["total"]
        return {
            "profit_total": profit_total,
            "profit_entries": len(profits),
            "financial_progress": financial_progress,
            "english_minutes": english_minutes,
            "english_hours": round(english_minutes / 60, 1),
            "english_days": len(english_dates),
            "english_streak": studied_streak,
            "daily_logs_count": len(enriched_logs),
            "good_days": sum(1 for log in enriched_logs if log["classification"] == "good"),
            "good_day_streak": current_streak(good_dates),
            "perfect_days": perfect_days,
            "average_daily_score": average_daily,
            "goal_progress": goal_progress,
            "weekly_completion_rate": round((sum(log["completed_habits"] for log in weekly_logs) / (len(weekly_logs) * len(BOOLEAN_FIELDS)) * 100), 1) if weekly_logs else 0.0,
            "monthly_completion_rate": round((sum(log["completed_habits"] for log in monthly_logs) / (len(monthly_logs) * len(BOOLEAN_FIELDS)) * 100), 1) if monthly_logs else 0.0,
            "classification_counts": dict(classification_counts),
            "weekly_habit_totals": weekly_habit_totals,
            "weekly_logs": weekly_logs,
            "monthly_logs": monthly_logs,
            "recent_logs": enriched_logs[:7],
            "recent_profits": list(reversed(profits[:10])),
            "recent_english": list(reversed(sessions[:10])),
            "recent_activity": recent_activity,
            "launch_count": launch_count,
            "unlocked_achievements": unlocked_count,
            "achievement_progress": round((unlocked_count / len(self.achievements.definitions())) * 100, 1),
            "today_log": today_log,
            "db_path": str(self.database.db_path),
            "settings": settings,
        }

    def refresh_achievements(self) -> list[str]:
        data = self.metrics()
        metrics = self._achievement_metric_snapshot(data)
        return self.achievements.evaluate(metrics)

    def achievement_status(self) -> list[dict[str, object]]:
        data = self.metrics()
        metrics = self._achievement_metric_snapshot(data)
        return self.achievements.all_with_status(metrics)

    def _achievement_metric_snapshot(self, data: dict[str, object]) -> dict[str, float]:
        return {
            "profit_total": data["profit_total"],
            "profit_entries": data["profit_entries"],
            "english_minutes": data["english_minutes"],
            "english_days": data["english_days"],
            "good_day_streak": data["good_day_streak"],
            "good_days": data["good_days"],
            "perfect_days": data["perfect_days"],
            "app_launches": data["launch_count"],
            "goal_progress": data["goal_progress"],
            "logs_count": data["daily_logs_count"],
        }

    def calendar_scores(self) -> dict[str, dict[str, object]]:
        settings = self.get_settings()
        data: dict[str, dict[str, object]] = {}
        for log in self.list_daily_logs():
            enriched = self._enrich_log(log, settings)
            data[log["log_date"]] = {
                "score": enriched["score"],
                "classification": enriched["classification"],
            }
        return data

    def get_enriched_log(self, log_date: str) -> dict[str, object] | None:
        log = self.get_daily_log(log_date)
        if not log:
            return None
        return self._enrich_log(log, self.get_settings())

    def _enrich_log(self, log: dict[str, object], settings: dict[str, object]) -> dict[str, object]:
        enriched = dict(log)
        enriched["completed_habits"] = sum(int(enriched.get(field, 0) or 0) for field in BOOLEAN_FIELDS)
        enriched["score"] = calculate_daily_score(enriched, settings)
        enriched["classification"] = classify_score(enriched["score"], settings)
        return enriched

    def _recent_activity(
        self,
        profits: list[dict[str, object]],
        sessions: list[dict[str, object]],
        logs: list[dict[str, object]],
    ) -> list[dict[str, str]]:
        activity: list[dict[str, str]] = []
        for row in profits[:6]:
            activity.append(
                {
                    "date": row["entry_date"],
                    "type": 'Earnings',
                    "title": row["source"],
                    "detail": f"R$ {float(row['amount']):.2f}",
                }
            )
        for row in sessions[:6]:
            activity.append(
                {
                    "date": row["session_date"],
                    "type": 'English',
                    "title": row["study_type"],
                    "detail": f"{int(row['duration_minutes'])} min",
                }
            )
        for row in logs[:6]:
            activity.append(
                {
                    "date": row["log_date"],
                    "type": 'Day',
                    "title": row["classification"],
                    "detail": f"Score {int(row['score'])}% / {int(row['completed_habits'])} habits",
                }
            )
        return sorted(activity, key=lambda item: item["date"], reverse=True)[:10]
