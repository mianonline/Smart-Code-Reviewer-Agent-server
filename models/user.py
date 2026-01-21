from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_length_bytes(cls, v: str) -> str:
        if v is None:
            return v
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long; must be at most 72 bytes when encoded. Please shorten your password.")
        return v

class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
