import streamlit as st
from graph import build_graph
from state import AgentState

st.set_page_config(page_title="JuniorDevs AI", layout="centered")

st.title("👨‍💻 JuniorDevs: Autonomous Code Generator")

task_input = st.text_area(
    "🧠 Enter a coding task",
    height=150,
    placeholder="e.g. Write a Python program to check if a number is prime"
)

if st.button("🚀 Generate Code"):
    with st.spinner("Running autonomous agents..."):

        graph = build_graph()
        initial_state = AgentState(task=task_input, retry_count=0)
        final_state = graph.invoke(initial_state)

        st.markdown("### ✅ Final Code:")
        st.code(final_state.get("code", ""), language=final_state.get("language", "text"))


        if final_state.get("error"):
            st.markdown("### ⚠️ Error:")
            st.code(final_state["error"])

        if final_state.get("feedback"):
            st.markdown("### 🧠 Feedback:")
            st.info(final_state["feedback"])

        if not final_state.get("is_verified", False):
            st.warning("❌ Final solution was not verified as logically correct.")
        else:
            st.success("✅ Final solution was approved!")
