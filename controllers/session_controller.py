from fastapi import HTTPException
from bson import ObjectId
from database import get_db
from models.chat import ChatSessionResponse

async def get_user_sessions(user_id: str):
    db_conn = get_db()
    cursor = db_conn.sessions.find({"user_id": user_id}).sort("created_at", -1)
    sessions = []
    async for doc in cursor:
        sessions.append(ChatSessionResponse(
            id=str(doc["_id"]),
            language=doc["language"],
            created_at=doc["created_at"],
            message_count=len(doc.get("messages", []))
        ))
    return sessions

async def get_session_by_id(session_id: str, user_id: str):
    db_conn = get_db()
    try:
        doc = await db_conn.sessions.find_one({"_id": ObjectId(session_id), "user_id": user_id})
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid session ID format")
         
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    
    doc["id"] = str(doc.pop("_id"))
    return doc

async def delete_session(session_id: str, user_id: str):
    db_conn = get_db()
    try:
        result = await db_conn.sessions.delete_one({"_id": ObjectId(session_id), "user_id": user_id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID format")
        
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found or permission denied")
    
    return {"message": "Session deleted successfully"}
