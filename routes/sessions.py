from fastapi import APIRouter, Depends
from typing import Annotated, List
from routes.deps import get_current_user
from models.chat import ChatSessionResponse
from controllers.session_controller import get_user_sessions, get_session_by_id

router = APIRouter(prefix="/api/sessions", tags=["sessions"])

@router.get("", response_model=List[ChatSessionResponse])
async def read_sessions(current_user: Annotated[dict, Depends(get_current_user)]):
    return await get_user_sessions(current_user["id"])

@router.get("/{session_id}")
async def read_session_detail(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return await get_session_by_id(session_id, current_user["id"])
