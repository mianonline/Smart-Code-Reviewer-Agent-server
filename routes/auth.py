from fastapi import APIRouter
from models.user import UserCreate, Token
from controllers.auth_controller import signup_user, signin_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    return await signup_user(user_data)

@router.post("/signin", response_model=Token)
async def signin(user_data: UserCreate):
    return await signin_user(user_data)
