from fastapi import FastAPI
from pydantic import BaseModel
from agent import chat
from llama_index.core.base.llms.types import ChatMessage

app = FastAPI()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.post("/chat")
async def agent_endpoint(request: ChatRequest):
    print(request.messages)

    messages = [ChatMessage(role=m.role, content=m.content) for m in request.messages]
    response = await chat(messages)
    return {"response": str(response)}
