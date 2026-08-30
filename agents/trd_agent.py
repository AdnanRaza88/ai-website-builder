from core.state import BuildState
from core.llm import LLMConfig, call_llm
from agents.prompts import TRD_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    try:
        trd = call_llm(config, TRD_SYSTEM, state["prd"])
    except Exception as exc:
        state["error"] = f"trd agent failed: {exc}"
        state["stage"] = "failed"
        return state

    state["trd"] = trd
    state["stage"] = "architecture"
    return state
