import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from config.mcp_servers import MCPServerSpec


class MCPManager:
    def __init__(self, servers: list[MCPServerSpec]):
        self.servers = {s.id: s for s in servers}
        self.sessions: dict[str, ClientSession] = {}
        self._stack: AsyncExitStack | None = None

    async def connect(self, server_id: str) -> ClientSession:
        if server_id in self.sessions:
            return self.sessions[server_id]

        spec = self.servers[server_id]
        params = StdioServerParameters(command=spec.command, args=spec.args, env=spec.env or None)

        if self._stack is None:
            self._stack = AsyncExitStack()

        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        self.sessions[server_id] = session
        return session

    async def call_tool(self, server_id: str, tool_name: str, arguments: dict):
        session = await self.connect(server_id)
        result = await session.call_tool(tool_name, arguments)
        return result

    async def list_tools(self, server_id: str):
        session = await self.connect(server_id)
        result = await session.list_tools()
        return result.tools

    async def close(self):
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
            self.sessions = {}


def call_tool_sync(manager: MCPManager, server_id: str, tool_name: str, arguments: dict):
    return asyncio.run(manager.call_tool(server_id, tool_name, arguments))


def list_tools_sync(manager: MCPManager, server_id: str):
    return asyncio.run(manager.list_tools(server_id))
