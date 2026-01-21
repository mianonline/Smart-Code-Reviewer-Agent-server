from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def performance_node(state: ReviewState, llm, parser):
    """Node focused on optimization and complexity"""
    prompt = ChatPromptTemplate.from_template(
        "You are a Performance Expert. Analyze this {language} code for performance issues.\n"
        "Look for: inefficient loops, unnecessary operations, memory leaks, complexity issues.\n\n"
        "Code:\n```{language}\n{code}\n```\n\n"
        "CRITICAL: You MUST respond with ONLY a valid JSON object. No markdown, no explanation, no text before or after.\n"
        "JSON format: {{\"issues\": [\"issue1\"], \"score\": 8, \"suggestions\": [\"suggestion1\"]}}\n"
        "Score: 1-10 (10 = best performance). If no issues, return empty arrays."
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "performance_issues": res.get("issues", []),
        "suggestions": res.get("suggestions", []),
        "scores": [res.get("score", 10)]
    }
