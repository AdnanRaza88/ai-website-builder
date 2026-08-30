import streamlit as st
from core.state import BuildState
from utils.file_export import build_zip_bytes


def render_specs(state: BuildState):
    if state["prd"]:
        with st.expander("PRD"):
            st.markdown(state["prd"])

    if state["trd"]:
        with st.expander("TRD"):
            st.markdown(state["trd"])

    if state["architecture"]:
        with st.expander("Architecture Plan"):
            st.json(state["architecture"])

    if state["review_notes"]:
        with st.expander("Review Notes"):
            for note in state["review_notes"]:
                st.markdown(f"- {note}")

    if state["generated_files"]:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### Generated Files")
        tabs = st.tabs(list(state["generated_files"].keys()))
        for tab, (path, content) in zip(tabs, state["generated_files"].items()):
            with tab:
                language = "html" if path.endswith(".html") else "css" if path.endswith(".css") else "javascript"
                st.code(content, language=language)
        st.markdown('</div>', unsafe_allow_html=True)

        zip_bytes = build_zip_bytes(state["generated_files"])
        st.download_button(
            "Download site as zip",
            data=zip_bytes,
            file_name="generated-website.zip",
            mime="application/zip",
            use_container_width=True,
        )
