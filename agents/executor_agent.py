# agents/executor_agent.py

import os
import requests
import base64
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()

class ExecutorAgent:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            temperature=0.3,
            max_tokens=200,
        )
        self.HEADERS = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        self.LANG_API = "https://judge0-ce.p.rapidapi.com/languages"
        self.SUBMIT_API = "https://judge0-ce.p.rapidapi.com/submissions"

    def get_all_languages(self) -> list:
        try:
            response = requests.get(self.LANG_API, headers=self.HEADERS, timeout=10)
            return response.json()
        except Exception as e:
            print(f"[ExecutorAgent] Failed to fetch Judge0 languages: {e}")
            return []

    def detect_language_id(self, task: str, languages: list) -> int:
        lang_list = "\n".join([f"{lang['id']}: {lang['name']}" for lang in languages])
        messages = [
            SystemMessage(content="""You are an AI assistant. Given a programming task and a list of supported Judge0 languages with IDs, choose the correct language_id to run the code. 
Only return the number. No explanation. No markdown."""),
            HumanMessage(content=f"""Available Languages:\n{lang_list}\n\nTask:\n{task}\n\nReturn the correct language_id only:""")
        ]

        try:
            response = self.llm.invoke(messages)
            return int(response.content.strip())
        except:
            return None

    def decode_b64(self, value):
        try:
            return base64.b64decode(value).decode() if value else ""
        except Exception:
            return value

    def execute_code(self, task: str, code: str, input_string: str = "") -> dict:
        languages = self.get_all_languages()
        language_id = self.detect_language_id(task, languages)

        if not language_id:
            return {
                "success": False,
                "output": None,
                "error": "Could not detect language_id via LLM."
            }

        encoded_code = base64.b64encode(code.encode()).decode()
        payload = {
            "language_id": language_id,
            "source_code": encoded_code,
            "stdin": input_string,
            "encode_source": True
        }

        try:
            res = requests.post(
                self.SUBMIT_API + "?base64_encoded=true&wait=true",
                json=payload,
                headers=self.HEADERS,
                timeout=15
            )
            result = res.json()
            language_name = next((l["name"] for l in languages if l["id"] == language_id), "unknown")

            return {
                "success": result.get("status", {}).get("id") == 3,
                "output": self.decode_b64(result.get("stdout")),
                "error": self.decode_b64(result.get("stderr") or result.get("compile_output")),
                "language_id": language_id,
                "language_name": language_name
            }

        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": f"Judge0 execution failed: {e}"
            }
