from datetime import datetime
from llama_index.core.tools import FunctionTool


def get_current_date():
    """Return the current date in ISO format."""
    return datetime.now().isoformat()


get_current_date_tool = FunctionTool.from_defaults(
    get_current_date,
)
