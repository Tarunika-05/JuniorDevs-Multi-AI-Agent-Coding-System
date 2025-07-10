# nodes/max_retries_node.py
from langsmith import traceable

@traceable(name="Max Retry Node")
def max_retries_node(state: dict) -> dict:
    return {
        **state,
        "final_answer": None,
        "stop_reason": "max_retries_suggest_user_refine_prompt",
        "feedback": "The system attempted 3 times but couldn’t generate correct logic. Please provide a more specific task description."
    }
