from llama_index.core.base.llms.types import ChatMessage
from .planner.planner import plan
from .executors.chat_executor import chat_execute
from .executors.sms_executor import sms_execute
from .preprocessor.precprocessor import preprocess
from .viewer.viewer import viewer
from .selector.selector import select


async def chat_agent(messages: list[ChatMessage] = []):
    if not messages:
        raise ValueError("No messages provided")
    if not isinstance(messages, list) or not all(
        isinstance(m, ChatMessage) for m in messages
    ):
        raise ValueError("Messages must be a list of ChatMessage objects")
    if len(messages) == 0:
        raise ValueError("No messages provided")

    primary_message = messages[-1].content or ""
    chat_history = []
    if len(messages) > 1:
        chat_history = messages[:-1]

    primary_message = preprocess(primary_message, chat_history)

    plan_response = await plan(primary_message, chat_history=chat_history)
    if plan_response:
        primary_message = f"{primary_message} \n\n Plan: {plan_response}"

    response = await chat_execute(primary_message, chat_history=chat_history)

    if response:
        messages.append(ChatMessage(role="assistant", content=str(response)))

    viewer_response = viewer(
        primary_message, chat_history=chat_history, agent_response=str(response)
    )

    if viewer_response != "NONE":
        response = {"type": "navigate", "data": viewer_response}

    return response


async def sms_agent(messages: list[ChatMessage] = []):
    if not messages:
        raise ValueError("No messages provided")
    if not isinstance(messages, list) or not all(
        isinstance(m, ChatMessage) for m in messages
    ):
        raise ValueError("Messages must be a list of ChatMessage objects")
    if len(messages) == 0:
        raise ValueError("No messages provided")

    primary_message = messages[-1].content or ""
    chat_history = []
    if len(messages) > 1:
        chat_history = messages[:-1]

    primary_message = preprocess(primary_message, chat_history)

    plan_response = await plan(primary_message, chat_history=chat_history)
    if plan_response:
        primary_message = f"{primary_message} \n\n Plan: {plan_response}"

    response = await sms_execute(primary_message, chat_history=chat_history)
    return response
