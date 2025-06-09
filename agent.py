from llama_index.core.base.llms.types import ChatMessage
from planner.planner import plan
from executor.executor import execute


async def chat(messages: list[ChatMessage] = []):
    if not messages:
        raise ValueError("No messages provided")
    if not isinstance(messages, list) or not all(
        isinstance(m, ChatMessage) for m in messages
    ):
        raise ValueError("Messages must be a list of ChatMessage objects")
    if len(messages) == 0:
        raise ValueError("No messages provided")

    primary_message = messages[-1].content
    chat_history = []
    if len(messages) > 1:
        chat_history = messages[:-1]

    plan_response = await plan(primary_message, chat_history=chat_history)
    if plan_response:
        primary_message = f"{primary_message} \n\n Plan: {plan_response}"

    response = await execute(primary_message, chat_history=chat_history)
    return response
