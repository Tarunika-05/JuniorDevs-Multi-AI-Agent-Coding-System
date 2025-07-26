# agents/engineer_agent.py

from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
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

    def extract_code_block(self, text: str) -> str:
        """Extracts code from a markdown-style code block."""
        match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        return match.group(1).strip() if match else text.strip()

    def generate_code(self, task: str, previous_code: str = None, feedback: str = None) -> dict:
        system_prompt = """
You are a structured code generator.

Determine the programming language based on the user's task.
Return ONLY a JSON object in this format:

{
  "language": "<programming language>",
  "code": "<multiline code>",
  "sample_input": "<example input>"
}

DO NOT use triple backticks or markdown formatting in any field.
DO NOT include explanations or extra text outside the JSON.
"""

        messages = [SystemMessage(content=system_prompt)]

        if previous_code and feedback:
            messages.append(HumanMessage(content=(
                f"Here is the previous code:\n{previous_code}\n\n"
                f"Feedback:\n{feedback}\n\n"
                "Revise the code based on feedback and return updated JSON as described."
            )))
        else:
            messages.append(HumanMessage(content=(
                f"Write code to solve this task:\n{task}\n"
                "Return only the JSON object in the format described."
            )))

        response = self.llm.invoke(messages)
        content = response.content.strip()

        try:
            # If model returns triple backticks anyway, clean them
            if content.startswith("```"):
                content = self.extract_code_block(content)

            result = json.loads(content)
            return result
        except Exception as e:
            raise ValueError(f"EngineerAgent: Failed to parse LLM response:\n{content}") from e
