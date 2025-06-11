from llama_index.core.base.llms.types import ChatMessage
from tools.tools import get_tools
from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4.1-mini")

SYSTEM_PROMPT = """\
You are an AI assistant for Paisa which is an application to record and track expenses/income.

Before you help a user, you need to work with tools to interact with our database.

Notes:
- Always show transactions in a table format with columns: date, label, amount. Amount should be negative for expenses and positive for income.
- Always show tags in a table format with columns: label.
- While searching transaction with date, always search with dates -1 day and +1 day.
- If year is not provided, assume the current year.
- If month is not provided, assume the current month.
- If day is not provided, assume the current day.
- Use startDate and endDate filters only if specified. DO NOT use them for terms similar to 'last record', 'previous record', etc.
- Do not send 'null' as argument for any tool. If a tool does not require an argument, simply do not include it in the function call.
"""


async def __create_executor_agent():
    tools = await get_tools()

    # Create the agent
    agent = FunctionCallingAgent.from_tools(
        llm=llm,
        tools=list(tools),
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
    )
    return agent


async def execute(message: str, chat_history: list[ChatMessage] = []):
    if not message:
        raise ValueError("No message provided")

    agent = await __create_executor_agent()

    response = await agent.achat(message, chat_history=chat_history)

    return response
