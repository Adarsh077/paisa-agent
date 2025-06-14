from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from src import config

mcp_client = BasicMCPClient(config.MCP_API_URL)
mcp_tool_spec = McpToolSpec(client=mcp_client)
