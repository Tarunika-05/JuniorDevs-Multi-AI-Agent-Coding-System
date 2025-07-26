# agents/engineer_agent.py

from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import ast
import re
import json
load_dotenv()

class EngineerAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            temperature=0.2,
            max_tokens=800,
        )

    def generate_code(self, task: str, previous_code: str = None, feedback: str = None) -> dict:
        messages = [
          SystemMessage(
    content="""
You are a helpful and structured code generator.

When you respond, return **only JSON** in this format:

{
  "language": "python",
  "code": "```python\\n<valid multiline code here>\\n```",
  "sample_input": "..."
}

Make sure the 'code' field includes line breaks and correct indentation, enclosed in triple backticks.
"""
)



        ]

        if previous_code and feedback:
            messages.append(HumanMessage(content=(
                f"You previously wrote this code:\n{previous_code}\n\n"
                f"However, the following feedback was given:\n{feedback}\n\n"
                "Please revise the code to address the issue and return the improved version "
                "in the format described above."
            )))
        else:
            messages.append(HumanMessage(content=(
                f"Write code to solve this task:\n{task}\n"
                "Do not include test input/output. Return the answer as a dictionary as described above."
            )))

        response = self.llm.invoke(messages)
        content = response.content.strip()

        
    try:
        result = json.loads(content)
        # Remove backticks from the "code" field after parsing
        if "code" in result:
            result["code"] = re.sub(r"^```(?:python)?\n?|```$", "", result["code"].strip())
            return result
    except Exception as e:
        raise ValueError(f"EngineerAgent: Failed to parse response: {response.content.strip()}") from e
