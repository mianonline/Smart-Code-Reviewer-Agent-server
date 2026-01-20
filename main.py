from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models.schemas import (
    CodeReviewRequest, 
    CodeReviewResponse, 
    HealthResponse, 
    CodeGenerationRequest, 
    CodeGenerationResponse,
    ChatRequest,
    ChatResponse
)
from services.code_analyzer import CodeAnalyzer
from utils.validators import CodeValidator
from config import settings
import uvicorn

app = FastAPI(
    title="Smart Code Reviewer API",
    description="API for AI-powered code review",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
analyzer = CodeAnalyzer()

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Smart Code Reviewer API is running. Visit /docs for documentation."}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running"
    }

@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Review code snippet
    """
    try:
        
        CodeValidator.sanitize_code(request.code)
        
        result = analyzer.analyze_code(request.code, request.language)
        
        return CodeReviewResponse(
            score=result["score"],
            issues=result["issues"],
            suggestions=result["suggestions"],
            reasoning=result["reasoning"],
            language=request.language
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc() 
        print(f"Error processing review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/review/file", response_model=CodeReviewResponse)
async def review_file(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    """
    Review uploaded code file
    """
    try:
        # Read content
        content = await file.read()
        
        # Validate size
        is_valid_size, size_msg = CodeValidator.validate_file_size(len(content))
        if not is_valid_size:
            raise HTTPException(status_code=400, detail=size_msg)
            
        # Validate extension
        is_valid_ext, ext_msg = CodeValidator.validate_file_extension(file.filename or "")
        if not is_valid_ext:
            raise HTTPException(status_code=400, detail=ext_msg)
            
        # Detect language if not provided
        detected_lang = CodeValidator.detect_language_from_extension(file.filename or "")
        final_lang = language if language else detected_lang
        
        if final_lang == 'unknown':
            raise HTTPException(status_code=400, detail="Could not detect language. Please specify.")
            
        # Decode content
        try:
            code_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be a valid text file")
            
        # Analyze
        result = analyzer.analyze_code(code_content, final_lang)
        
        return CodeReviewResponse(
            score=result["score"],
            issues=result["issues"],
            suggestions=result["suggestions"],
            reasoning=result["reasoning"],
            language=final_lang
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """
    Generate code from prompt
    """
    try:
        result = analyzer.generate_code(request.prompt, request.language)
        return CodeGenerationResponse(
            code=result["code"],
            explanation=result["explanation"],
            language=request.language
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat_followup(request: ChatRequest):
    """
    Follow-up chat about a code review
    """
    try:
        # Convert Request model messages to list of dicts
        history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response_content = analyzer.chat(
            code=request.code,
            review_context=request.review_context,
            messages=history,
            language=request.language
        )
        return ChatResponse(content=response_content)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
