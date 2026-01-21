from pydantic import BaseModel, Field, validator
from typing import List, Optional

class CodeReviewRequest(BaseModel):
    """Request model for code review"""
    code: str = Field(..., min_length=1, description="Code to be reviewed")
    language: str = Field(..., description="Programming language (javascript, typescript, python)")
    
    @validator('language')
    def validate_language(cls, v):
        allowed_languages = ['javascript', 'typescript', 'python', 'html', 'css', 'json', 'c', 'cpp', 'php']
        if v.lower() not in allowed_languages:
            raise ValueError(f'Language must be one of: {", ".join(allowed_languages)}')
        return v.lower()
    
    @validator('code')
    def validate_code(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Code cannot be empty')
        return v

class CodeReviewResponse(BaseModel):
    """Response model for code review"""
    score: int = Field(..., ge=0, le=10, description="Code quality score (0-10)")
    issues: List[str] = Field(default_factory=list, description="List of identified issues")
    suggestions: List[str] = Field(default_factory=list, description="List of improvement suggestions")
    reasoning: str = Field(..., description="Detailed explanation of the score and feedback")
    language: str = Field(..., description="Programming language analyzed")
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str

class CodeGenerationRequest(BaseModel):
    """Request model for code generation"""
    prompt: str = Field(..., min_length=1, description="Description of the code to generate")
    language: str = Field(..., description="Target programming language")

class CodeGenerationResponse(BaseModel):
    """Response model for code generation"""
    code: str = Field(..., description="The generated code")
    explanation: str = Field(..., description="Explanation of how the code works")
    language: str = Field(..., description="Programming language used")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    """Request model for follow-up chat"""
    code: str = Field(..., description="The code context")
    review_context: str = Field(..., description="The previous review feedback")
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    language: str = Field(..., description="Programming language")
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Response model for chat"""
    content: str = Field(..., description="AI's response")
