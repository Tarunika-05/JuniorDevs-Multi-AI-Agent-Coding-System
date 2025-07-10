from langsmith import traceable
from agents.verifier_agent import VerifierAgent

verifier = VerifierAgent()

@traceable(name="Verifier Node")
def verifier_node(state: dict) -> dict:
    result = verifier.verify(
        task=state["task"],
        code=state["code"],
        language=state.get("language", "unknown")
    )

    return {
        **state,
        "is_verified": result["is_logically_correct"],
        "feedback": result["feedback"]
    }
