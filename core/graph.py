from langgraph.graph import StateGraph, END
from core.state import BuildState
from core.llm import LLMConfig
from agents import requirements_agent, prd_agent, trd_agent, architect_agent, coder_agent, reviewer_agent

TERMINAL_STAGES = {"awaiting_user", "done", "failed"}


def build_graph(config: LLMConfig):
    graph = StateGraph(BuildState)

    graph.add_node("requirements", lambda s: requirements_agent.run(s, config))
    graph.add_node("prd", lambda s: prd_agent.run(s, config))
    graph.add_node("trd", lambda s: trd_agent.run(s, config))
    graph.add_node("architecture", lambda s: architect_agent.run(s, config))
    graph.add_node("coding", lambda s: coder_agent.run(s, config))
    graph.add_node("reviewing", lambda s: reviewer_agent.run(s, config))

    def route(state: BuildState) -> str:
        if state["stage"] in TERMINAL_STAGES:
            return END
        return state["stage"]

    graph.set_conditional_entry_point(route)
    for node in ["requirements", "prd", "trd", "architecture", "coding", "reviewing"]:
        graph.add_conditional_edges(node, route)

    return graph.compile()


def run_step(state: BuildState, config: LLMConfig) -> BuildState:
    compiled = build_graph(config)
    result = compiled.invoke(state, config={"recursion_limit": 100})
    return result
