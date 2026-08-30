import uuid
import streamlit as st

from storage.db import init_db
from storage.session_store import ensure_user, save_session_state, load_session_state
from core.state import new_state
from core.llm import LLMConfig
from core.graph import run_step
from ui.styles import GLASS_CSS
from ui.sidebar import render_sidebar
from ui.chat_view import render_chat
from ui.spec_view import render_specs

st.set_page_config(page_title="AI Website Builder", layout="wide")
st.markdown(GLASS_CSS, unsafe_allow_html=True)

init_db()

query_params = st.query_params
user_token = query_params.get("u")
if not user_token:
    user_token = uuid.uuid4().hex[:12]
    st.query_params["u"] = user_token

ensure_user(user_token)

session_id = query_params.get("s")
if not session_id:
    session_id = f"{user_token}-{uuid.uuid4().hex[:8]}"
    st.query_params["s"] = session_id

settings_values = render_sidebar(user_token)

stored_state = load_session_state(session_id)
if stored_state is None:
    state = new_state(user_token, session_id)
else:
    state = stored_state

st.title("AI Website Builder")
st.caption("Describe your website idea and the agent team will plan, build and review it.")

left, right = st.columns([1, 1])

with left:
    render_chat(state)

    if not settings_values["api_key"]:
        st.warning("Add your provider API key in Settings before starting.")

    user_input = st.chat_input("Describe your website or answer the agent's question")

    if user_input and settings_values["api_key"]:
        state["conversation"].append({"role": "user", "content": user_input})
        if state["stage"] in ("awaiting_user", "collecting_requirements"):
            state["stage"] = "collecting_requirements"
        elif state["stage"] == "failed":
            state["error"] = None

        config = LLMConfig(
            provider_id=settings_values["provider_id"],
            model_name=settings_values["model_name"],
            api_key=settings_values["api_key"],
            base_url=settings_values["base_url"] or None,
        )

        with st.spinner("Agents are working"):
            state = run_step(state, config)

        save_session_state(session_id, user_token, state)
        st.rerun()

with right:
    render_specs(state)
