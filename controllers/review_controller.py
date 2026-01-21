from fastapi import HTTPException, UploadFile
from datetime import datetime
from database import get_db
from services.code_analyzer import CodeAnalyzer
from utils.validators import CodeValidator
from models.schemas import CodeReviewResponse, CodeGenerationResponse

analyzer = CodeAnalyzer()

async def analyze_code(code: str, language: str, user_id: str):
    try:
        CodeValidator.sanitize_code(code)
        result = analyzer.analyze_code(code, language)
        
        # Save to DB
        db_conn = get_db()
        session = {
            "user_id": user_id,
            "language": language,
            "code": code,
            "score": result["score"],
            "issues": result["issues"],
            "suggestions": result["suggestions"],
            "reasoning": result["reasoning"],
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        res = await db_conn.sessions.insert_one(session)
        
        return CodeReviewResponse(
            score=result["score"],
            issues=result["issues"],
            suggestions=result["suggestions"],
            reasoning=result["reasoning"],
            language=language,
            session_id=str(res.inserted_id)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error processing review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def analyze_file(file: UploadFile, language: str = None):
    try:
        content = await file.read()
        
        is_valid_size, size_msg = CodeValidator.validate_file_size(len(content))
        if not is_valid_size:
            raise HTTPException(status_code=400, detail=size_msg)
            
        is_valid_ext, ext_msg = CodeValidator.validate_file_extension(file.filename or "")
        if not is_valid_ext:
            raise HTTPException(status_code=400, detail=ext_msg)
            
        detected_lang = CodeValidator.detect_language_from_extension(file.filename or "")
        final_lang = language if language else detected_lang
        
        if final_lang == 'unknown':
            raise HTTPException(status_code=400, detail="Could not detect language. Please specify.")
            
        try:
            code_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be a valid text file")
            
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

def generate_code_response(prompt: str, language: str):
    try:
        result = analyzer.generate_code(prompt, language)
        return CodeGenerationResponse(
            code=result["code"],
            explanation=result["explanation"],
            language=language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
