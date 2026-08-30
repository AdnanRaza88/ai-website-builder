from core.state import BuildState
from core.llm import LLMConfig, call_llm
from agents.prompts import CODER_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    files = state["architecture"].get("files", [])
    design_notes = state["architecture"].get("design_notes", "")
    review_notes = "\n".join(state["review_notes"])

    generated: dict[str, str] = {}
    for file_spec in files:
        path = file_spec["path"]
        purpose = file_spec.get("purpose", "")
        prompt = (
            f"TRD:\n{state['trd']}\n\n"
            f"Design notes:\n{design_notes}\n\n"
            f"File to generate: {path}\n"
            f"Purpose: {purpose}\n\n"
            f"Review notes to address:\n{review_notes if review_notes else 'none'}"
        )
        try:
            content = call_llm(config, CODER_SYSTEM, prompt)
        except Exception as exc:
            state["error"] = f"coder agent failed on {path}: {exc}"
            state["stage"] = "failed"
            return state
        generated[path] = content

    state["generated_files"] = generated
    state["stage"] = "reviewing"
    return state
