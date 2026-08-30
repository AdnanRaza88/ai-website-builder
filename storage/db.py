import sqlite3
from contextlib import contextmanager
from config.settings import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_token TEXT PRIMARY KEY,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS user_settings (
    user_token TEXT PRIMARY KEY,
    provider_id TEXT,
    model_name TEXT,
    api_key TEXT,
    base_url TEXT,
    custom_instructions TEXT,
    FOREIGN KEY(user_token) REFERENCES users(user_token)
);
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_token TEXT,
    state_json TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_token) REFERENCES users(user_token)
);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
