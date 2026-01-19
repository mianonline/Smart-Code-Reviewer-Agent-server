import json
from openai import OpenAI
from typing import Dict, Any
from config import settings

class CodeAnalyzer:    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code and return structured feedback
        """
        prompt = self._build_review_prompt(code, language)
        
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior software engineer conducting a thorough code review. You must respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                max_tokens=2000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            
            print(f"DEBUG: OpenAI API Call failed ({str(e)}). Using Mock Mode.")
            return {
                "score": 8,
                "issues": [
                    "Naming convention could be more descriptive for the main function.",
                    "Missing type hints which makes the code harder to maintain.",
                    "Potential optimization possible in the loop structure."
                ],
                "suggestions": [
                    "Use snake_case for Python functions as per PEP 8.",
                    "Add return type annotations to your functions.",
                    "Consider using a list comprehension for better performance."
                ],
                "reasoning": f"Your code is functional and well-structured. I am providing this mock response because your OpenAI API reported: '{str(e)[:50]}...'. This allows you to test the UI beauty and flow while you sort out the API billing."
            }

    def generate_code(self, prompt: str, language: str) -> Dict[str, Any]:
        """
        Generate code based on a prompt
        """
        system_prompt = f"You are an expert {language} developer. Generate clean, efficient, and well-documented code. You must respond with valid JSON only."
        user_prompt = f"""Task: {prompt}
Language: {language}

You must respond with a JSON object in this exact format:
{{
    "code": "<the generated code string>",
    "explanation": "<brief explanation of how the code works>",
    "language": "{language}"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={ "type": "json_object" },
                max_tokens=2000
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"DEBUG: OpenAI Generation API Call failed ({str(e)}). Using Mock Mode.")
            return {
                "code": f"// Mock code for: {prompt}\nfunction example() {{\n  console.log('AI Generation is currently in mock mode.');\n}}",
                "explanation": "This is a fallback response since the OpenAI API encountered an error.",
                "language": language
            }
    
    def _build_review_prompt(self, code: str, language: str) -> str:
        """Build the user prompt for code review"""
        return f"""Analyze the following {language.upper()} code and provide constructive feedback.

Code to review:
```{language}
{code}
```

You must respond with a JSON object in this format:
{{
    "score": <number 0-10>,
    "issues": [<list of strings>],
    "suggestions": [<list of strings>],
    "reasoning": "<detailed explanation>"
}}

Scoring criteria:
- 0-3: Critical issues
- 4-6: Needs improvement
- 7-8: Good quality
- 9-10: Excellent/Clean code
"""
