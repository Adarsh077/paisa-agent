from llama_index.core.base.llms.types import ChatMessage
from src.tools.tools import get_tools
from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4.1-mini")

SYSTEM_PROMPT = """\
You are the "Agent Selector" for a simple, non-technical finance management app.
Every request by the user must be analyzed to decide which helper agents need to be used for that request.
The agents are:

Executor Agent: needed for adding/changing data
Display Agent: needed for showing data in list format
Given any user query, output a single list of agent names to fulfill the request, in this order: executor, display.
Do not output any explanations, only the list.

Examples: 

"List all transactions from last month." → display
"I spent 10 on gas." → executor
"I spent 10 on gas and show me my recent transactions." → executor,display
"What's my balance?" → executor
"Add an account." → executor
"""


async def __create_selector_agent():
    tools = await get_tools()

    agent = FunctionCallingAgent.from_tools(
        llm=llm,
        max_function_calls=0,
        tools=list(tools),
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
    )
    return agent


async def select(message: str, chat_history: list[ChatMessage] = []):
    if not message:
        raise ValueError("No message provided")

    agent = await __create_selector_agent()

    response = await agent.achat(message, chat_history=chat_history)
    return str(response).split(",") if response else []
