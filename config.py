import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 1024 * 1024 
    ALLOWED_EXTENSIONS: set = {".js", ".ts", ".py"}
    
    # Scoring Criteria
    SCORE_CRITERIA = {
        "excellent": (9, 10),
        "good": (7, 8),
        "improvable": (4, 6),
        "poor": (0, 3)
    }

settings = Settings()
