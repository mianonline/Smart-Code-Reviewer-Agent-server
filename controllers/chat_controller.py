from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId
from database import get_db
from controllers.review_controller import analyzer

async def chat_followup_logic(code: str, review_context: str, messages: list, language: str, session_id: str = None, user_id: str = None):
    try:
        # history = [{"role": msg.role, "content": msg.content} for msg in messages] # handled in route
        
        response_content = analyzer.chat(
            code=code,
            review_context=review_context,
            messages=messages,
            language=language
        )
        
        if session_id and user_id:
            db_conn = get_db()
            user_msg = messages[-1]
            ai_msg = {"role": "assistant", "content": response_content}
            
            await db_conn.sessions.update_one(
                {"_id": ObjectId(session_id), "user_id": user_id},
                {
                    "$push": {"messages": {"$each": [user_msg, ai_msg]}},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
        return response_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
