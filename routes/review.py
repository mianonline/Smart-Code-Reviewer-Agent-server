from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Annotated, Optional
from routes.deps import get_current_user
from models.schemas import CodeReviewRequest, CodeReviewResponse, CodeGenerationRequest, CodeGenerationResponse
from controllers.review_controller import analyze_code, analyze_file, generate_code_response

router = APIRouter(prefix="/api", tags=["review"])

@router.post("/review", response_model=CodeReviewResponse)
async def review_endpoint(
    request: CodeReviewRequest,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return await analyze_code(request.code, request.language, current_user["id"])

@router.post("/review/file", response_model=CodeReviewResponse)
async def review_file_endpoint(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    return await analyze_file(file, language)

@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_endpoint(request: CodeGenerationRequest):
    return generate_code_response(request.prompt, request.language)
