from fastapi import HTTPException
from database import get_db
from models.user import UserCreate
from utils.auth import get_password_hash, verify_password, create_access_token
import secrets

async def signup_user(user_data: UserCreate):
    db_conn = get_db()
    if db_conn is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    # Check if user exists
    existing_user = await db_conn.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Create user
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["id"] = secrets.token_hex(12)
    
    await db_conn.users.insert_one(user_dict)
    
    # Create token
    access_token = create_access_token(data={"sub": user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}

async def signin_user(user_data: UserCreate):
    db_conn = get_db()
    if db_conn is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    
    user = await db_conn.users.find_one({"email": user_data.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    access_token = create_access_token(data={"sub": user_data.email})
    return {"access_token": access_token, "token_type": "bearer"}
