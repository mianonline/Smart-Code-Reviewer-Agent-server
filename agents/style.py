from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def style_node(state: ReviewState, llm, parser):
    """Node focused on clean code, naming, and PEP/Style guides"""
    prompt = ChatPromptTemplate.from_template(
        "Clean Code Architect: Analyze this {language} code for readability, naming, and style.\n"
        "Return JSON: {{\"issues\": [string], \"score\": int, \"suggestions\": [string]}}\nCode:\n```{language}\n{code}\n```"
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "style_issues": res.get("issues", []),
        "suggestions": res.get("suggestions", []),
        "scores": [res.get("score", 10)]
    }
