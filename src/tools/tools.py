from datetime import datetime
from typing import Sequence, Optional
from llama_index.core.tools import FunctionTool, BaseTool
from src.tools.mcp_client import get_mcp_tool_spec


def get_current_date():
    """Return the current date in ISO format."""
    return datetime.now().isoformat()


get_current_date_tool = FunctionTool.from_defaults(
    get_current_date,
)


async def get_tools(jwt_token: Optional[str] = None) -> Sequence[BaseTool]:
    mcp_tool_spec = get_mcp_tool_spec(jwt_token)
    mcp_tools = await mcp_tool_spec.to_tool_list_async()
    mcp_tools.append(get_current_date_tool)
    return mcp_tools
