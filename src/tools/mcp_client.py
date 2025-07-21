from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from src import config
from typing import Optional


class AuthenticatedMCPClient(BasicMCPClient):
    """Custom MCP client that passes JWT token to tool calls"""

    def __init__(self, url: str, jwt_token: Optional[str] = None):
        super().__init__(url)
        self.jwt_token = jwt_token

    async def call_tool(self, name: str, arguments: dict = None):
        """Override call_tool to pass JWT token"""
        if arguments is None:
            arguments = {}

        # Add JWT token to arguments if available
        if self.jwt_token:
            arguments["jwt_token"] = self.jwt_token

        return await super().call_tool(name, arguments)


def get_mcp_tool_spec(jwt_token: Optional[str] = None) -> McpToolSpec:
    """Get MCP tool spec with optional JWT token"""
    mcp_client = AuthenticatedMCPClient(config.MCP_API_URL, jwt_token)
    return McpToolSpec(client=mcp_client)
