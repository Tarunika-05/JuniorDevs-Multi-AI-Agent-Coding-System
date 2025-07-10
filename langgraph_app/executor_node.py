from langsmith import traceable
from agents.executor_agent import ExecutorAgent

executor = ExecutorAgent()

@traceable(name="Executor Node")
def executor_node(state: dict) -> dict:
    print("🛠️ Executing the generated code...")

    result = executor.execute_code(
        task=state["task"],
        code=state["code"],
        input_string=state.get("input", "")
    )

    # ❗ Check the error from this execution, not from previous state
    if result["error"]:
        return {
            **state,
            "output": result["output"],
            "error": result["error"],
            "language": result.get("language_name"),
            "language_id": result.get("language_id"),
            "is_correct": False,
            "feedback": f"Execution failed with error: {result['error']}"
        }

    return {
        **state,
        "output": result["output"],
        "error": "",  
        "language": result.get("language_name"),
        "language_id": result.get("language_id"),
    }
