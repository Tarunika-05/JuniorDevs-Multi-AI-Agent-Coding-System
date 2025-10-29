import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

class VerifierAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            temperature=0.3,
            max_tokens=800,
        )

    def verify(self, task: str, code: str, language: str = "unknown") -> dict:
        messages = [
            SystemMessage(content="""You are a senior developer. Your job is to check if the provided code logically solves the given task, even if the output looks correct.

Return your answer ONLY as JSON in the following format:

{
  "is_logically_correct": true or false,
  "feedback": "Explain clearly whether the code truly solves the task or not."
}
""")
        ]

        user_prompt = f"""
Task:
{task}

Language:
{language}

Code:
{code}

Check whether the logic of the code is correct and complete, regardless of whether it produced output.
"""

        messages.append(HumanMessage(content=user_prompt))

        response = self.llm.invoke(messages)
        content = response.content.strip()

        try:
            parsed = json.loads(content)
            return {
                "is_logically_correct": parsed.get("is_logically_correct", False),
                "feedback": parsed.get("feedback", "No feedback returned.")
            }
        except json.JSONDecodeError:
            return {
                "is_logically_correct": False,
                "feedback": f"Failed to parse verifier response:\n{content}"
            }
