from core.state import BuildState
from core.llm import LLMConfig, call_llm_json
from agents.prompts import ARCHITECT_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    try:
        plan = call_llm_json(config, ARCHITECT_SYSTEM, state["trd"])
    except Exception as exc:
        state["error"] = f"architect agent failed: {exc}"
        state["stage"] = "failed"
        return state

    state["architecture"] = plan
    state["stage"] = "coding"
    return state
