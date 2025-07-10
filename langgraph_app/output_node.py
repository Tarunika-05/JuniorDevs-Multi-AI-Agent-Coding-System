# nodes/output_node.py
from langsmith import traceable

@traceable(name="Output Node")
def output_node(state: dict) -> dict:
    return {
        **state,
        "final_answer": state.get("code"),
        "stop_reason": "success"
    }
