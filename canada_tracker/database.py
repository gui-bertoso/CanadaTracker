from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from canada_tracker.config import DEFAULT_SETTINGS, encode_setting, ensure_data_dir, parse_setting


class Database:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = ensure_data_dir(db_path)
        self._init_db()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS profit_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    source TEXT NOT NULL,
                    entry_date TEXT NOT NULL,
                    note TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS english_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    duration_minutes INTEGER NOT NULL,
                    study_type TEXT NOT NULL,
                    session_date TEXT NOT NULL,
                    note TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS daily_logs (
                    log_date TEXT PRIMARY KEY,
                    water INTEGER NOT NULL DEFAULT 0,
                    ate_well INTEGER NOT NULL DEFAULT 0,
                    trained INTEGER NOT NULL DEFAULT 0,
                    studied_english INTEGER NOT NULL DEFAULT 0,
                    worked_progress INTEGER NOT NULL DEFAULT 0,
                    slept_well INTEGER NOT NULL DEFAULT 0,
                    cardio INTEGER NOT NULL DEFAULT 0,
                    mobility INTEGER NOT NULL DEFAULT 0,
                    mood INTEGER,
                    weight REAL,
                    note TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS achievement_unlocks (
                    achievement_id TEXT PRIMARY KEY,
                    unlocked_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS app_launches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    launched_at TEXT NOT NULL
                );
                """
            )
            for key, value in DEFAULT_SETTINGS.items():
                conn.execute(
                    "INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)",
                    (key, encode_setting(value)),
                )

    def record_launch(self) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO app_launches(launched_at) VALUES(?)",
                (datetime.now().isoformat(timespec="seconds"),),
            )

    def get_settings(self) -> dict[str, object]:
        with self.connect() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
        settings = dict(DEFAULT_SETTINGS)
        for row in rows:
            default = DEFAULT_SETTINGS.get(row["key"], row["value"])
            settings[row["key"]] = parse_setting(row["value"], default)
        return settings

    def save_settings(self, updates: dict[str, object]) -> None:
        with self.connect() as conn:
            for key, value in updates.items():
                conn.execute(
                    """
                    INSERT INTO settings(key, value)
                    VALUES(?, ?)
                    ON CONFLICT(key) DO UPDATE SET value = excluded.value
                    """,
                    (key, encode_setting(value)),
                )
