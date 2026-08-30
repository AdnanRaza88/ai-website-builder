from dataclasses import dataclass, field
from config.settings import settings


@dataclass(frozen=True)
class MCPServerSpec:
    id: str
    label: str
    command: str
    args: list[str]
    env: dict[str, str] = field(default_factory=dict)
    description: str = ""


def build_registry(sandbox_dir: str, github_token: str) -> list[MCPServerSpec]:
    return [
        MCPServerSpec(
            "filesystem",
            "Filesystem",
            "npx",
            ["-y", "@modelcontextprotocol/server-filesystem", sandbox_dir],
            description="write and read the generated site files",
        ),
        MCPServerSpec(
            "fetch",
            "Fetch",
            "uvx",
            ["mcp-server-fetch"],
            description="pull reference content from the web",
        ),
        MCPServerSpec(
            "git",
            "Git",
            "uvx",
            ["mcp-server-git", "--repository", sandbox_dir],
            description="initialize and commit the generated project",
        ),
        MCPServerSpec(
            "github",
            "GitHub",
            "npx",
            ["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token},
            description="push the generated project to a new repository",
        ),
        MCPServerSpec(
            "memory",
            "Knowledge Graph Memory",
            "npx",
            ["-y", "@modelcontextprotocol/server-memory"],
            description="short term scratchpad for the current build session",
        ),
        MCPServerSpec(
            "sequential_thinking",
            "Sequential Thinking",
            "npx",
            ["-y", "@modelcontextprotocol/server-sequential-thinking"],
            description="structured reasoning for architecture and review",
        ),
        MCPServerSpec(
            "time",
            "Time",
            "uvx",
            ["mcp-server-time"],
            description="timestamps for changelog entries",
        ),
        MCPServerSpec(
            "mempalace",
            "MemPalace",
            "uvx",
            ["mempalace", "mcp-server", "--data-dir", settings.mempalace_data_dir],
            description="long term memory across sessions for a user",
        ),
    ]
