from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.chat_service import generate_answer

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    async def event_stream():
        async for chunk in generate_answer(request.session_id, request.message):
            yield f"data: {chunk}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")