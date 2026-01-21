from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def style_node(state: ReviewState, llm, parser):
    """Node focused on clean code, naming, and PEP/Style guides"""
    prompt = ChatPromptTemplate.from_template(
        "You are a Code Style Expert. Analyze this {language} code for style and readability.\n"
        "Look for: naming conventions, code organization, comments, best practices.\n\n"
        "Code:\n```{language}\n{code}\n```\n\n"
        "CRITICAL: You MUST respond with ONLY a valid JSON object. No markdown, no explanation, no text before or after.\n"
        "JSON format: {{\"issues\": [\"issue1\"], \"score\": 8, \"suggestions\": [\"suggestion1\"]}}\n"
        "Score: 1-10 (10 = cleanest code). If no issues, return empty arrays."
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "style_issues": res.get("issues", []),
        "suggestions": res.get("suggestions", []),
        "scores": [res.get("score", 10)]
    }
