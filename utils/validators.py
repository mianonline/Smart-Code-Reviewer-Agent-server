import os
from pathlib import Path
from typing import Tuple
from config import settings

class CodeValidator:
    """Validator for code input and file uploads"""
    
    @staticmethod
    def validate_file_size(file_size: int) -> Tuple[bool, str]:
        """Validate file size is within limits"""
        if file_size > settings.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE / (1024 * 1024)}MB"
        return True, "Valid file size"
    
    @staticmethod
    def validate_file_extension(filename: str) -> Tuple[bool, str]:
        """Validate file extension is allowed"""
        file_ext = Path(filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            return False, f"File extension {file_ext} not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        return True, "Valid file extension"
    
    @staticmethod
    def detect_language_from_extension(filename: str) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.js': 'javascript',
            '.ts': 'typescript',
            '.py': 'python'
        }
        file_ext = Path(filename).suffix.lower()
        return ext_to_lang.get(file_ext, 'unknown')
    
    @staticmethod
    def sanitize_code(code: str) -> str:
        """Sanitize code input (basic cleanup)"""
        return code.strip()
