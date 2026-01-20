from langchain_core.prompts import ChatPromptTemplate
from .state import ReviewState

def performance_node(state: ReviewState, llm, parser):
    """Node focused on optimization and complexity"""
    prompt = ChatPromptTemplate.from_template(
        "Performance Guru: Analyze this {language} code for inefficiencies or complexity issues.\n"
        "Return JSON: {{\"issues\": [string], \"score\": int, \"suggestions\": [string]}}\nCode:\n```{language}\n{code}\n```"
    )
    chain = prompt | llm | parser
    res = chain.invoke({"code": state["code"], "language": state["language"]})
    return {
        "performance_issues": res.get("issues", []),
        "suggestions": res.get("suggestions", []),
        "scores": [res.get("score", 10)]
    }
