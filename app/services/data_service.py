import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from app.models.schemas import ChatMessage

DB_PATH = Path("data/chatbot.db")


class DataService:
    """Simple SQL + pandas + numpy utility service for analytics and persistence."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._bootstrap()

    def _bootstrap(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def log_chat_event(self, user_id: str, session_id: str, message: str, response: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO chat_events (user_id, session_id, user_message, bot_response)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, session_id, message, response),
            )

    def append_message(self, session_id: str, role: str, content: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content),
            )

    def get_recent_messages(self, session_id: str, limit: int = 10) -> list[ChatMessage]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT role, content
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()

        return [ChatMessage(role=role, content=content) for role, content in reversed(rows)]

    def conversation_stats(self) -> dict[str, float]:
        query = "SELECT user_message, bot_response FROM chat_events"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return {"turns": 0.0, "avg_user_len": 0.0, "avg_bot_len": 0.0}

        user_lengths = df["user_message"].str.len().to_numpy(dtype=float)
        bot_lengths = df["bot_response"].str.len().to_numpy(dtype=float)

        return {
            "turns": float(len(df)),
            "avg_user_len": float(np.mean(user_lengths)),
            "avg_bot_len": float(np.mean(bot_lengths)),
        }
