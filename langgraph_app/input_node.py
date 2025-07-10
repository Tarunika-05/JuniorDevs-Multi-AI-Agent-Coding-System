# nodes/input_node.py
from langsmith import traceable

@traceable(name="Input Node")

def input_node(state: dict) -> dict:
    """
    This node simply passes the initial input state to the rest of the graph.
    You can add validation, logging, or preprocessing here if needed.
    """
    return state
