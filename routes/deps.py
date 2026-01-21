from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from database import get_db
from utils.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    db_conn = get_db()
    if db_conn is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
        
    user = await db_conn.users.find_one({"email": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
