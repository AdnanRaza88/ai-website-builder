import streamlit as st
from config.providers import provider_labels, get_provider
from storage.session_store import save_user_settings, load_user_settings


def render_sidebar(user_token: str) -> dict:
    st.sidebar.markdown("### AI Website Builder")
    existing = load_user_settings(user_token) or {}

    with st.sidebar.popover("⚙ Settings", use_container_width=True):
        st.markdown("**Model Provider**")
        labels = provider_labels()
        ids = [i for i, _ in labels]
        default_index = ids.index(existing["provider_id"]) if existing.get("provider_id") in ids else 0
        provider_id = st.selectbox(
            "Provider",
            options=ids,
            format_func=lambda i: dict(labels)[i],
            index=default_index,
        )
        spec = get_provider(provider_id)

        model_name = st.text_input("Model name", value=existing.get("model_name") or spec.default_model)
        api_key = st.text_input("API key", value=existing.get("api_key") or "", type="password")
        base_url = ""
        if spec.needs_base_url:
            base_url = st.text_input("Base URL", value=existing.get("base_url") or "")

        custom_instructions = st.text_area(
            "Custom instructions",
            value=existing.get("custom_instructions") or "",
            placeholder="Any preferences the agents should always follow",
        )

        if st.button("Save settings", use_container_width=True):
            save_user_settings(user_token, provider_id, model_name, api_key, base_url, custom_instructions)
            st.success("Saved")
            st.rerun()

    return {
        "provider_id": provider_id,
        "model_name": model_name,
        "api_key": api_key,
        "base_url": base_url,
        "custom_instructions": custom_instructions,
    }
