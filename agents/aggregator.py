from .state import ReviewState

def aggregator_node(state: ReviewState):
    """Compiles all agent findings into a single final response"""
    all_issues = state["security_issues"] + state["performance_issues"] + state["style_issues"]
    avg_score = sum(state["scores"]) // len(state["scores"]) if state["scores"] else 8
    
    reasoning = (
        f"Security analysis found {len(state['security_issues'])} issues. "
        f"Performance analysis flagged {len(state['performance_issues'])} optimization points. "
        f"Clean code review identified {len(state['style_issues'])} style improvements."
    )

    return {
        "final_result": {
            "score": avg_score,
            "issues": all_issues,
            "suggestions": state["suggestions"],
            "reasoning": reasoning,
            "language": state["language"]
        }
    }
