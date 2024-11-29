import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

client = OpenAI(api_key="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")
class ChatRequest(BaseModel):
    model: str
    messages: list


@app.post("/chat")
async def chat_completion(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=request.messages,
            stream=True,
        )

        async def stream():
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        return StreamingResponse(stream(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
