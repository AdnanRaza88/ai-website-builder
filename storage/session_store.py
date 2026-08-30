import json
from storage.db import get_conn


def ensure_user(user_token: str):
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO users (user_token) VALUES (?)", (user_token,))


def save_user_settings(user_token: str, provider_id: str, model_name: str, api_key: str, base_url: str, custom_instructions: str):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO user_settings (user_token, provider_id, model_name, api_key, base_url, custom_instructions)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_token) DO UPDATE SET
                provider_id=excluded.provider_id,
                model_name=excluded.model_name,
                api_key=excluded.api_key,
                base_url=excluded.base_url,
                custom_instructions=excluded.custom_instructions
            """,
            (user_token, provider_id, model_name, api_key, base_url, custom_instructions),
        )


def load_user_settings(user_token: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM user_settings WHERE user_token = ?", (user_token,)
        ).fetchone()
        return dict(row) if row else None


def save_session_state(session_id: str, user_token: str, state: dict):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO sessions (session_id, user_token, state_json)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                state_json=excluded.state_json,
                updated_at=CURRENT_TIMESTAMP
            """,
            (session_id, user_token, json.dumps(state)),
        )


def load_session_state(session_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT state_json FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        return json.loads(row["state_json"]) if row else None


def list_sessions_for_user(user_token: str) -> list[str]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT session_id FROM sessions WHERE user_token = ? ORDER BY updated_at DESC",
            (user_token,),
        ).fetchall()
        return [r["session_id"] for r in rows]
