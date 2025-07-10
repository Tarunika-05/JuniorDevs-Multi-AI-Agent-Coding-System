from langgraph.graph import StateGraph, END
from state import AgentState

# Import node functions
from langgraph_app.input_node import input_node
from langgraph_app.engineer_node import engineer_node
from langgraph_app.executor_node import executor_node
from langgraph_app.critic_node import critic_node
from langgraph_app.verifier_node import verifier_node
from langgraph_app.output_node import output_node
from langgraph_app.max_retries_node import max_retries_node


def build_graph():
    # Step 1: Create the graph object with the defined state schema
    graph = StateGraph(AgentState)

    # Step 2: Register nodes in the graph
    graph.add_node("input", input_node)

    # 👇 Engineer now returns code + language metadata (filename, run_cmd, etc.)
    graph.add_node("engineer", engineer_node)

   
    graph.add_node("executor", executor_node)

    graph.add_node("critic", critic_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("output", output_node)
    graph.add_node("max_retries", max_retries_node)

    # Step 3: Set entry point of the graph
    graph.set_entry_point("input")

    # Step 4: Define transitions between nodes
    graph.add_edge("input", "engineer")
    graph.add_edge("engineer", "executor")
    graph.add_edge("executor", "critic")

    # After critic: decide whether to retry or proceed to verifier
    def critic_check(state: AgentState):
        if not state["is_correct"]:
            print("\n🔍 Problem detected by ❌ Critic:")
            print(f"🗣 Feedback: {state['feedback']}")
            if state["retry_count"] < 3:
                print("🔁 Returning to Engineer for revision...\n")
                return "engineer"
            else:
                print("❌ Max retries reached. Ending.")
                return "max_retries"
        print("✅ Critic approved the output. Proceeding to Verifier...\n")
        return "verifier"


    graph.add_conditional_edges("critic", critic_check)

    # After verifier: decide whether to output or retry
    def verifier_check(state: AgentState):
        if state["is_verified"]:
            print("✅ Verifier confirmed the logic is correct.\n🎉 Final approval granted.\n")
            return "output"
        else:
            print("\n🧠 Verifier identified a logic issue:")
            print(f"🗣 Feedback: {state['feedback']}")
            if state["retry_count"] < 3:
                print("🔁 Returning to Engineer for logic fix...\n")
                return "engineer"
            else:
                print("❌ Max retries reached. Ending.")
                return "max_retries"

    graph.add_conditional_edges("verifier", verifier_check)

    # Step 5: Define terminal (end) nodes
    graph.set_finish_point("output")
    graph.set_finish_point("max_retries")

    # Step 6: Compile the graph for execution
    return graph.compile()
