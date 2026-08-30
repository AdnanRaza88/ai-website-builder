from config.mcp_servers import build_registry
from config.settings import settings
from mcp.client import MCPManager, call_tool_sync


def get_manager(sandbox_dir: str, github_token: str) -> MCPManager:
    registry = build_registry(sandbox_dir, github_token)
    return MCPManager(registry)


def remember(manager: MCPManager, user_token: str, content: str, tags: list[str] | None = None):
    return call_tool_sync(
        manager,
        "mempalace",
        "mempalace_remember",
        {"wing": user_token, "content": content, "tags": tags or []},
    )


def recall(manager: MCPManager, user_token: str, query: str, limit: int = 5):
    return call_tool_sync(
        manager,
        "mempalace",
        "mempalace_recall",
        {"wing": user_token, "query": query, "limit": limit},
    )


def build_context_summary(manager: MCPManager, user_token: str, topic: str) -> str:
    try:
        result = recall(manager, user_token, topic)
    except Exception:
        return ""
    if not result:
        return ""
    return str(result)
