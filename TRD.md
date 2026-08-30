# Technical Requirements Document

## Stack
- Python 3.11
- Streamlit for UI
- LangGraph for agent orchestration
- LangChain for prompt and message primitives
- LiteLLM for unified access to multiple LLM providers
- MCP Python SDK for tool servers
- MemPalace for long term agent memory, run as a local MCP server
- SQLite for session and settings persistence

## Architecture
The system is a single Streamlit process. State machine logic lives in core/graph.py as a LangGraph StateGraph with one dispatch node and seven agent nodes. Each Streamlit rerun calls graph.invoke on the persisted state and stops either at END or at the awaiting_user stage, so a full page refresh never loses progress because state is reloaded from SQLite before the graph runs.

## Agent Nodes
1. requirements_agent — extracts structured requirements from the conversation, decides if more questions are needed.
2. prd_agent — writes PRD.md content from requirements.
3. trd_agent — writes TRD.md content from the PRD.
4. architect_agent — plans the file tree and component boundaries.
5. coder_agent — writes actual file contents for every planned file.
6. reviewer_agent — checks generated files against the TRD and architecture plan, approves or requests changes.

## Loop Control
loop_count increments every time reviewer_agent sends work back to coder_agent. When loop_count reaches settings.max_agent_loops the graph forces stage to done and surfaces the best available output with a warning rather than looping forever.

## MCP Servers
| Server | Transport | Purpose |
|---|---|---|
| filesystem | stdio | write generated files to a sandboxed directory |
| fetch | stdio | pull reference content and images from the web |
| git | stdio | initialize a git repo for the generated project |
| github | stdio | push the generated project to a new repository |
| memory | stdio | short term knowledge graph scratchpad for the current build |
| sequential-thinking | stdio | structured multi step reasoning for the architect and reviewer agents |
| time | stdio | timestamps for generated changelog entries |
| mempalace | stdio | long term memory across sessions for a given user token |

## Provider Model
Every provider is defined once in config/providers.py with an id, a LiteLLM prefix and the environment variable name it expects. The user selects a provider in the sidebar, pastes their own key, and the key is stored per user token in SQLite. No provider key ships with the app.

## Persistence Model
users(user_token) — one row per browser session token.
user_settings(user_token) — provider choice, model, api key, base url, custom instructions.
sessions(session_id, user_token, state_json) — the full BuildState serialized as JSON, updated after every graph step.

## Failure Handling
Every agent node wraps its LLM call in a try block. On failure the node sets stage to awaiting_user with a pending_question describing the failure so the user sees it immediately instead of a blank screen.
