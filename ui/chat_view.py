import streamlit as st
from core.state import BuildState


def render_chat(state: BuildState):
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f'<span class="glass-badge">{state["stage"].replace("_", " ").title()}</span>', unsafe_allow_html=True)

    for message in state["conversation"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    if state["stage"] == "failed" and state["error"]:
        st.error(state["error"])

    if state["loop_count"] > 0 and state["stage"] not in ("done", "failed"):
        st.caption(f"Review loop {state['loop_count']} of the current build")
