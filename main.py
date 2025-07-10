# main.py

import os
from dotenv import load_dotenv
from graph import build_graph  # Your LangGraph workflow builder

# Load environment variables
load_dotenv()

# ✅ Ensure LangSmith is set for tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "junior-devs"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# ✅ Build the LangGraph workflow
graph = build_graph()

def main():
    print("👨‍💻 Welcome to JuniorDevs: Your Autonomous Code Generator\n")
    task_input = input("🧠 Enter a coding task you'd like to solve: ").strip()

    if not task_input:
        print("❌ No task provided. Exiting.")
        return

    # Initial state for the graph
    state = {
        "task": task_input,
        "attempt_count": 0,
        "retry_count": 0,
        "code": "",
        "output": "",
        "error": "",
        "is_correct": False,
        "is_verified": False,
        "reasoning": ""
    }

    print("\n🚀 Running autonomous coding flow...\n")
    final_state = graph.invoke(state)

    # ✅ Final results
    print("✅ Final Code:\n")
    print(final_state.get("code", "[No code returned]"))

    print("\n🧠 Final Reasoning / Feedback:\n")
    print(final_state.get("reasoning", "[No reasoning provided]"))

    if final_state.get("error"):
        print("\n⚠️ Execution Error:\n")
        print(final_state["error"])

if __name__ == "__main__":
    main()
