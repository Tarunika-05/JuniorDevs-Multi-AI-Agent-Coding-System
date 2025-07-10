import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

class CriticAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            temperature=0.2,
            max_tokens=800,
        )

    def critique(
        self,
        task: str,
        code: str,
        output: str = None,
        error: str = None,
        language: str = "unknown"
    ) -> dict:
        messages = [
            SystemMessage(content="""
You are a strict and objective code reviewer. Your job is to decide if the code output is fully correct for the given task.

Return your response ONLY as a JSON object in this format:

{
  "is_correct": true or false,
  "feedback": "Explain briefly and clearly."
}
""")
        ]

        if error:
            user_prompt = f"""
Task:
{task}

Language:
{language}

Code:
{code}

❌ It failed to execute with the following error:
{error}

Please identify the cause of the failure and explain how to fix it.
"""
        else:
            user_prompt = f"""
Task:
{task}

Language:
{language}

Code:
{code}

✅ It executed successfully and produced this output:
{output}

Is this output correct for the given task? If not, explain what went wrong and how to fix it.
"""

        messages.append(HumanMessage(content=user_prompt))

        response = self.llm.invoke(messages)
        content = response.content.strip()

        try:
            parsed = json.loads(content)
            return {
                "is_correct": parsed.get("is_correct", False),
                "feedback": parsed.get("feedback", "No feedback returned.")
            }
        except json.JSONDecodeError:
            return {
                "is_correct": False,
                "feedback": f"Failed to parse JSON response. Raw content:\n{content}"
            }
