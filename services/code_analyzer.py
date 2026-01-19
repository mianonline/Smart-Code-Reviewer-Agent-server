import json
from typing import Dict, Any
from config import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class CodeAnalyzer:    
    def __init__(self):
        # Initialize LangChain model
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0.2
        )
        self.parser = JsonOutputParser()
    
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code and return structured feedback using LangChain
        """
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are a senior software engineer conducting a thorough code review. You must respond with valid JSON only."),
                ("user", self._get_review_prompt_template())
            ])
            
            # Create a chain: Prompt -> LLM -> Parser
            chain = prompt_template | self.llm | self.parser
            
            result = chain.invoke({
                "code": code,
                "language": language.upper()
            })
            
            return result
            
        except Exception as e:
            # Fallback to Mock Data if API fails
            print(f"DEBUG: LangChain/OpenAI API Call failed ({str(e)}). Using Mock Mode.")
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
                "reasoning": f"Your code is functional and well-structured. I am providing this mock response because your AI service reported: '{str(e)[:50]}...'. This allows you to test the UI beauty and flow while you sort out the API configuration."
            }

    def generate_code(self, prompt: str, language: str) -> Dict[str, Any]:
        """
        Generate code based on a prompt using LangChain
        """
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an expert {language} developer. Generate clean, efficient, and well-documented code. You must respond with valid JSON only."),
                ("user", self._get_generation_prompt_template())
            ])
            
            chain = prompt_template | self.llm | self.parser
            
            result = chain.invoke({
                "prompt": prompt,
                "language": language
            })
            
            return result
            
        except Exception as e:
            print(f"DEBUG: LangChain Generation API Call failed ({str(e)}). Using Mock Mode.")
            return {
                "code": f"// Mock code for: {prompt}\nfunction example() {{\n  console.log('AI Generation is currently in mock mode.');\n}}",
                "explanation": "This is a fallback response since the AI service encountered an error.",
                "language": language
            }
    
    def _get_review_prompt_template(self) -> str:
        """Instruction template for code review"""
        return """Analyze the following {language} code and provide constructive feedback.

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

    def _get_generation_prompt_template(self) -> str:
        """Instruction template for code generation"""
        return """Task: {prompt}
Language: {language}

You must respond with a JSON object in this exact format:
{{
    "code": "<the generated code string>",
    "explanation": "<brief explanation of how the code works>",
    "language": "{language}"
}}
"""
