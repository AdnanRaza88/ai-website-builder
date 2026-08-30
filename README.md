# AI Website Builder

Agentic spec driven website builder. Streamlit UI, LangGraph orchestration, LiteLLM for provider access, MCP servers for tools, MemPalace for long term agent memory.

## Local Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install the MCP servers used by the tool layer:

```
npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-github @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
uv tool install mcp-server-fetch
uv tool install mcp-server-git
uv tool install mcp-server-time
uv tool install mempalace
```

Copy `.env.example` to `.env` and fill in `GITHUB_PERSONAL_ACCESS_TOKEN` if you want the GitHub MCP server to work.

Run the app:

```
streamlit run app.py
```

## Deployment

Push this repository to GitHub, then deploy on Streamlit Community Cloud pointing at `app.py`. No secrets need to be set at platform level since every user supplies their own provider API key inside the app.

## Optional Landing Page

The `landing/` folder is a standalone static page you can publish on GitHub Pages. Update `APP_URL` in `landing/script.js` to your deployed Streamlit URL before publishing. It is a marketing entry point only, the actual app is fully self contained in Streamlit.

## Project Structure

```
app.py                  entrypoint
config/                 settings, provider registry, mcp server registry
core/                   state schema, llm wrapper, langgraph state machine
agents/                 one file per agent node
mcp/                    mcp client manager
memory/                 mempalace wrapper
storage/                sqlite persistence
ui/                     streamlit components and styling
utils/                  file export helpers
landing/                static marketing page for GitHub Pages
PRD.md                  product requirements for this project
TRD.md                  technical requirements for this project
```
