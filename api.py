from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import chat
import asyncio

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.post("/chat")
async def agent_endpoint(request: ChatRequest):
    print(request.messages)
    # Convert pydantic models to llama_index ChatMessage objects
    from llama_index.core.base.llms.types import ChatMessage

    messages = [ChatMessage(role=m.role, content=m.content) for m in request.messages]
    response = await chat(messages)
    return {"response": str(response)}
