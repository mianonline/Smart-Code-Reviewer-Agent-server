import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = [o.strip().strip('"').strip("'") for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
    
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
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY: str = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET", "")

settings = Settings()
