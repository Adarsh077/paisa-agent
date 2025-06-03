from llama_index.core.base.llms.types import ChatMessage
from tools.tools import get_tools
from llama_index.core.agent import FunctionCallingAgent
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4.1-mini")

SYSTEM_PROMPT = """\
You are an AI assistant for Paisa which is an application to record and track expenses/income.

Before you help a user, you need to work with tools to interact with our database.
"""


async def __create_executor_agent():
    tools = await get_tools()

    # Create the agent
    agent = FunctionCallingAgent.from_tools(
        llm=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
        memory=None,  # No memory for the executor agent
        state=None,  # No state for the executor agent
    )
    return agent


async def execute(message: ChatMessage, chat_history: list[ChatMessage] = []):
    print("a", message)
    if not message:
        raise ValueError("No message provided")

    agent = await __create_executor_agent()

    response = await agent.achat(message.content, chat_history=chat_history)

    return response
