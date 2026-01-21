from fastapi import HTTPException
from database import get_db
from datetime import datetime
from config import settings
import hashlib
import time

async def get_user_profile(email: str):
    db_conn = get_db()
    user = await db_conn.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove sensitive data
    user.pop("hashed_password", None)
    if "_id" in user:
        user["id"] = str(user.pop("_id"))
    return user

async def update_user_profile(email: str, profile_data: dict):
    db_conn = get_db()
    
    # Valid fields to update
    allowed_fields = ["full_name", "avatar_url", "username"]
    update_dict = {k: v for k, v in profile_data.items() if k in allowed_fields}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    update_dict["updated_at"] = datetime.utcnow()
    
    await db_conn.users.update_one(
        {"email": email},
        {"$set": update_dict}
    )
    
    updated_user = await db_conn.users.find_one({"email": email})
    updated_user.pop("hashed_password", None)
    if "_id" in updated_user:
        updated_user["id"] = str(updated_user.pop("_id"))
    return updated_user

def generate_cloudinary_signature():
    if not settings.CLOUDINARY_API_SECRET or not settings.CLOUDINARY_CLOUD_NAME:
        raise HTTPException(status_code=500, detail="Cloudinary not configured")
    
    timestamp = int(time.time())
    folder = "avatars"
    
    # Create signature string
    params_to_sign = f"folder={folder}&timestamp={timestamp}"
    signature = hashlib.sha256(
        (params_to_sign + settings.CLOUDINARY_API_SECRET).encode()
    ).hexdigest()
    
    return {
        "signature": signature,
        "timestamp": timestamp,
        "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
        "api_key": settings.CLOUDINARY_API_KEY,
        "folder": folder
    }
