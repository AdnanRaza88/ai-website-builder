from core.state import BuildState
from core.llm import LLMConfig, call_llm_json
from agents.prompts import REQUIREMENTS_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in state["conversation"])
    try:
        result = call_llm_json(config, REQUIREMENTS_SYSTEM, transcript)
    except Exception as exc:
        state["error"] = f"requirements agent failed: {exc}"
        state["stage"] = "failed"
        return state

    state["requirements"] = result.get("requirements", state["requirements"])
    state["requirements_complete"] = result.get("requirements_complete", False)

    if state["requirements_complete"]:
        state["stage"] = "prd"
        state["pending_question"] = None
    else:
        question = result.get("next_question") or "Can you share more detail about the website you want?"
        state["pending_question"] = question
        state["conversation"].append({"role": "assistant", "content": question})
        state["stage"] = "awaiting_user"

    return state
