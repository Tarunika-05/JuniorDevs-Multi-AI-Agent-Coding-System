from typing import TypedDict, Optional

class AgentState(TypedDict):
    task: str
    code: Optional[str]
    output: Optional[str]
    error: Optional[str]
    feedback: Optional[str]
    is_correct: Optional[bool]
    is_verified: Optional[bool]
    retry_count: int
    final_answer: Optional[str]
    stop_reason: Optional[str]
    language: Optional[str]
