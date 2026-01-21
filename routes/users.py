from fastapi import APIRouter, Depends
from typing import Annotated
from routes.deps import get_current_user
from controllers.user_controller import get_user_profile, update_user_profile, generate_cloudinary_signature

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me")
async def read_user_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return await get_user_profile(current_user["email"])

@router.put("/me")
async def update_user_me(
    profile_data: dict,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return await update_user_profile(current_user["email"], profile_data)

@router.get("/cloudinary/signature")
async def cloudinary_signature(current_user: Annotated[dict, Depends(get_current_user)]):
    return generate_cloudinary_signature()
