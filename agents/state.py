import operator
from typing import Dict, Any, List, TypedDict, Annotated

class ReviewState(TypedDict):
    code: str
    language: str
    # Agents will append their findings here
    security_issues: Annotated[List[str], operator.add]
    performance_issues: Annotated[List[str], operator.add]
    style_issues: Annotated[List[str], operator.add]
    suggestions: Annotated[List[str], operator.add]
    scores: Annotated[List[int], operator.add]
    final_result: Dict[str, Any]
