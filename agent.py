import asyncio
from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms.openai import OpenAI
from mcp_client import mcp_tool_spec

llm = OpenAI(model="gpt-4.1-nano", temperature=0)

SYSTEM_PROMPT = """\
You are an AI assistant for Paisa which is an application to record and track expenses/income.

Before you help a user, you need to work with tools to interact with Our Database
"""


async def create_agent():
    mcp_tools = await mcp_tool_spec.to_tool_list_async()

    # Create the agent
    agent = FunctionCallingAgent.from_tools(
        llm=llm,
        tools=mcp_tools,
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
    )
    return agent


async def chat(messages: list[ChatMessage] = []):
    if not messages:
        raise ValueError("No messages provided")
    if not isinstance(messages, list) or not all(
        isinstance(m, ChatMessage) for m in messages
    ):
        raise ValueError("Messages must be a list of ChatMessage objects")
    if len(messages) == 0:
        raise ValueError("No messages provided")

    agent = await create_agent()

    primary_message = messages[0].content
    chat_history = []
    if len(messages) > 1:
        chat_history = messages[1:]

    response = await agent.achat(primary_message, chat_history=chat_history)
    return response
