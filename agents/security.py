from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def security_node(state: ReviewState, llm, parser):
    """Node focused on security vulnerabilities"""
    prompt = ChatPromptTemplate.from_template(
        "Security Expert: Analyze this {language} code for vulnerabilities (SQLi, XSS, etc.).\n"
        "Return JSON: {{\"issues\": [string], \"score\": int}}\nCode:\n```{language}\n{code}\n```"
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "security_issues": res.get("issues", []),
        "scores": [res.get("score", 10)]
    }
