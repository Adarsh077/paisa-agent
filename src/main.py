from fastapi import FastAPI
from pydantic import BaseModel
from .agents import chat_agent, sms_agent
from llama_index.core.base.llms.types import ChatMessage
import json
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.post("/chat")
async def agent_endpoint(request: ChatRequest):
    messages = [ChatMessage(role=m.role, content=m.content) for m in request.messages]
    response = await chat_agent(messages)
    # For chat agent, return the response as plain text
    return {"response": str(response)}


@app.post("/sms")
async def sms_agent_endpoint(request: ChatRequest):
    messages = [ChatMessage(role=m.role, content=m.content) for m in request.messages]
    response = await sms_agent(messages)

    # SMS agent returns JSON string, so we need to parse it
    try:
        response_str = str(response)
        logger.info(f"Raw SMS response: {response_str}")

        # Try to parse as JSON
        parsed_response = json.loads(response_str)
        return parsed_response
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse SMS response as JSON: {e}")
        logger.error(f"Response content: {response_str}")
        # Fallback: return error response
        return {"status": "error", "message": "Failed to process SMS response"}
    except Exception as e:
        logger.error(f"Unexpected error processing SMS response: {e}")
        return {"status": "error", "message": "Internal server error"}
