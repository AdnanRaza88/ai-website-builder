import json
from core.state import BuildState
from core.llm import LLMConfig, call_llm
from agents.prompts import PRD_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    try:
        prd = call_llm(config, PRD_SYSTEM, json.dumps(state["requirements"]))
    except Exception as exc:
        state["error"] = f"prd agent failed: {exc}"
        state["stage"] = "failed"
        return state

    state["prd"] = prd
    state["stage"] = "trd"
    return state
