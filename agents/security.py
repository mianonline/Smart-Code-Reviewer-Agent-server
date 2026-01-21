from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def security_node(state: ReviewState, llm, parser):
    """Node focused on security vulnerabilities"""
    prompt = ChatPromptTemplate.from_template(
        "You are a Security Expert. Analyze this {language} code for security vulnerabilities.\n"
        "Look for: SQL injection, XSS, path traversal, hardcoded secrets, etc.\n\n"
        "Code:\n```{language}\n{code}\n```\n\n"
        "CRITICAL: You MUST respond with ONLY a valid JSON object. No markdown, no explanation, no text before or after.\n"
        "JSON format: {{\"issues\": [\"issue1\", \"issue2\"], \"score\": 8}}\n"
        "Score: 1-10 (10 = most secure). If no issues, return empty array for issues."
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "security_issues": res.get("issues", []),
        "scores": [res.get("score", 10)]
    }
