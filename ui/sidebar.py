import streamlit as st
from config.providers import provider_labels, get_provider, resolve_model_options
from storage.session_store import save_user_settings, load_user_settings


def render_sidebar(user_token: str) -> dict:
    st.sidebar.markdown("### AI Website Builder")
    existing = load_user_settings(user_token) or {}

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Settings**")

    labels = provider_labels()
    ids = [i for i, _ in labels]
    default_index = ids.index(existing["provider_id"]) if existing.get("provider_id") in ids else 0

    provider_id = st.sidebar.selectbox(
        "Provider",
        options=ids,
        format_func=lambda i: dict(labels)[i],
        index=default_index,
        key="provider_select",
    )
    spec = get_provider(provider_id)

    api_key = st.sidebar.text_input(
        "API key",
        value=existing.get("api_key") or "",
        type="password",
        key="api_key_input",
    )

    base_url = ""
    if spec.needs_base_url:
        base_url = st.sidebar.text_input(
            "Base URL",
            value=existing.get("base_url") or spec.default_base_url or "",
            key="base_url_input",
            help=f"Default: {spec.default_base_url}" if spec.default_base_url else None,
        )
    elif existing.get("base_url") and existing.get("provider_id") == provider_id:
        base_url = existing.get("base_url") or ""

    model_options, source = resolve_model_options(provider_id, api_key, base_url)
    if not model_options:
        model_options = [spec.default_model]

    saved_model = existing.get("model_name") or spec.default_model
    if saved_model not in model_options:
        model_options = [saved_model] + model_options

    try:
        model_index = model_options.index(saved_model)
    except ValueError:
        model_index = 0

    model_name = st.sidebar.selectbox(
        "Model",
        options=model_options,
        index=min(model_index, len(model_options) - 1),
        key="model_select",
        help=f"Source: {source}. Prefer models that support chat/completions.",
    )

    st.sidebar.caption(f"Models: {source} ({len(model_options)})")

    with st.sidebar.expander("Custom model override"):
        custom = st.text_input(
            "Type a model id if not in the list",
            value="",
            placeholder=spec.default_model,
            key="custom_model_input",
        )
        if custom.strip():
            model_name = custom.strip()
            st.info(f"Using custom model: `{model_name}`")

    custom_instructions = st.sidebar.text_area(
        "Custom instructions",
        value=existing.get("custom_instructions") or "",
        placeholder="Any preferences the agents should always follow",
        key="custom_instructions_input",
    )

    if st.sidebar.button("Save settings", use_container_width=True, type="primary"):
        save_user_settings(
            user_token,
            provider_id,
            model_name,
            api_key,
            base_url,
            custom_instructions,
        )
        st.sidebar.success("Saved")
        st.rerun()

    if provider_id == "opencode_zen":
        st.sidebar.caption(
            "Tip: free models like `deepseek-v4-flash`, `big-pickle`, `glm-4.7-free` "
            "use the chat/completions endpoint. If a model shows unavailable, pick another from the list."
        )

    return {
        "provider_id": provider_id,
        "model_name": model_name,
        "api_key": api_key,
        "base_url": base_url,
        "custom_instructions": custom_instructions,
    }
