import json
from config.settings import settings
from core.state import BuildState
from core.llm import LLMConfig, call_llm_json
from agents.prompts import REVIEWER_SYSTEM


def run(state: BuildState, config: LLMConfig) -> BuildState:
    payload = {
        "trd": state["trd"],
        "architecture": state["architecture"],
        "files": state["generated_files"],
    }
    try:
        result = call_llm_json(config, REVIEWER_SYSTEM, json.dumps(payload))
    except Exception as exc:
        state["error"] = f"reviewer agent failed: {exc}"
        state["stage"] = "failed"
        return state

    approved = result.get("approved", False)
    notes = result.get("notes", [])
    state["review_notes"] = notes
    state["review_approved"] = approved

    if approved:
        state["stage"] = "done"
        return state

    state["loop_count"] += 1
    if state["loop_count"] >= settings.max_agent_loops:
        state["stage"] = "done"
        state["review_notes"].append(
            "loop limit reached, delivering best available version"
        )
        return state

    state["stage"] = "coding"
    return state
