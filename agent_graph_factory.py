# agent_graph_factory.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List
from langchain_core.messages import BaseMessage
import operator


# --- 1. Define the Agent's State ---
# This TypedDict defines the structure of the "state" that will be passed
# between the nodes of our graph. The `operator.add` annotation tells LangGraph
# to append new messages to the existing list, rather than overwriting it.
class AgentState(TypedDict):
    messages: List[BaseMessage]


# --- 2. The Factory Function ---
# This function is our reusable "factory" for creating a new agent graph.
# It takes the LLM and a list of tools as input and wires them together
# into a coherent reasoning loop.
def build_agent_graph(llm, tools):
    """
    Builds the LangGraph agent graph using a robust, standard pattern.
    """
    # --- 3. Initialize the Graph ---
    # We initialize a StateGraph with our AgentState structure. This graph will
    # manage the agent's state as it moves from step to step.
    graph_builder = StateGraph(AgentState)

    # --- 4. Define the Graph Nodes ---
    # Each node is a function or a runnable that performs an action.

    # The `call_model` node is the "brain" of the agent. It takes the current
    # state and decides the next action (e.g., call a tool or respond to the user).
    def call_model(state):
        # We use .bind_tools to make the LLM aware of the available tools.
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # The `tool_node` is the "hands" of the agent. It's a pre-built node from
    # LangGraph that knows how to execute the tools called by the `call_model` node.
    tool_node = ToolNode(tools)

    # The `should_continue` function is the "router" or "dispatcher". It checks the
    # last message from the model and decides where to go next.
    def should_continue(state):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            # If the model made a tool call, we go to the tool_node.
            return "continue"
        # Otherwise, the agent has finished its work.
        return "end"

    # --- 5. Wire the Nodes Together ---
    # This is where we define the structure of the agent's reasoning loop.
    graph_builder.add_node("call_model", call_model)
    graph_builder.add_node("call_tools", tool_node)

    # The entry point is the first node to be called.
    graph_builder.set_entry_point("call_model")

    # The conditional edge directs the flow based on the router's decision.
    graph_builder.add_conditional_edges(
        "call_model", should_continue, {"continue": "call_tools", "end": END}
    )

    # This edge creates the essential loop: after the tools are called,
    # the flow goes *back* to the model to process the tool results.
    graph_builder.add_edge("call_tools", "call_model")

    # --- 6. Compile and Return the Graph ---
    # .compile() finalizes the graph, creating a runnable object that we
    # can use in our main application scripts.
    return graph_builder.compile()
