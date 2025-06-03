from datetime import datetime
from llama_index.core.tools import FunctionTool
from tools.mcp_client import mcp_tool_spec


def get_current_date():
    """Return the current date in ISO format."""
    return datetime.now().isoformat()


get_current_date_tool = FunctionTool.from_defaults(
    get_current_date,
)


async def get_tools():
    mcp_tools = await mcp_tool_spec.to_tool_list_async()
    mcp_tools.append(get_current_date_tool)
