from fastapi import APIRouter, Depends
from typing import Annotated
from routes.deps import get_current_user
from models.schemas import ChatRequest, ChatResponse
from controllers.chat_controller import chat_followup_logic

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    response_content = await chat_followup_logic(
        code=request.code,
        review_context=request.review_context,
        messages=history,
        language=request.language,
        session_id=request.session_id,
        user_id=current_user["id"]
    )
    
    return ChatResponse(content=response_content)
