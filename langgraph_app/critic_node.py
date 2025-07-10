from langsmith import traceable
from agents.critic_agent import CriticAgent

critic = CriticAgent()

@traceable(name="Critic Node")
def critic_node(state: dict) -> dict:
    error = state.get("error", "")
    output = state.get("output", "")
    code = state.get("code", "")
    task = state.get("task", "")
    language = state.get("language", "unknown")

    # 🛑 Force retry if error exists
    if error:
        print("👀 Critic received error:", error)
        return {
            **state,
            "is_correct": False,
            "feedback": f"The code failed with error:\n{error}"
        }

    # ✅ If no error, call the actual critic LLM
    print("👀 Critic received output:", output)
    result = critic.critique(
        task=task,
        code=code,
        output=output,
        error=None,  # don't send error again
        language=language
    )

    return {
        **state,
        "is_correct": result["is_correct"],
        "feedback": result["feedback"]
    }
