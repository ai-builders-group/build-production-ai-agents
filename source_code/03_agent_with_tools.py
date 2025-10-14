# 03_agent_with_tools.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List

# Import our new tool
from tools.word_counter import count_words

# --- 1. Load Environment Variables ---
load_dotenv()


# --- 2. Define the Agent's State ---
# We are adding a new key, `tool_calls`, to store the LLM's decision to use a tool.
class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage | ToolMessage]
    tool_calls: List[dict]  # LangGraph uses this to route to the ToolNode


# --- 3. Define the Nodes ---
# The LLM "brain" of our agent. It will decide whether to respond or use a tool.
def call_model(state: AgentState):
    """A node that calls the LLM to generate a response or a tool call."""
    print("---CALLING THE MODEL---")
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-flash",
    )

    # We bind our tool to the LLM. This makes the LLM "aware" of the tool.
    llm_with_tools = llm.bind_tools([count_words])

    response = llm_with_tools.invoke(state["messages"])

    # LangGraph will automatically route to the ToolNode if `tool_calls` is present.
    return {"messages": [response], "tool_calls": response.tool_calls}


# The node that executes the tools our agent decides to use.
tool_node = ToolNode([count_words])


# --- 4. Define the Edges (The Logic Flow) ---
def should_continue(state: AgentState):
    """
    The "Router". This function decides whether to continue using tools
    or to end the process and respond to the user.
    """
    print("---ASSESSING RESPONSE---")
    if state["tool_calls"]:
        # The LLM has requested to use a tool.
        return "continue"
    else:
        # The LLM has provided a final answer.
        return "end"


# --- 5. Build the Graph ---
graph_builder = StateGraph(AgentState)

# Add the nodes
graph_builder.add_node("call_model", call_model)
graph_builder.add_node("call_tools", tool_node)

# Set the entry point
graph_builder.set_entry_point("call_model")

# Add the conditional edge - this is the core of the ReAct loop
graph_builder.add_conditional_edges(
    "call_model",
    should_continue,
    {
        "continue": "call_tools",  # If tools are called, go to the tool node
        "end": END,  # If no tools, end the graph
    },
)

# Add the normal edge to loop back from the tool node to the model
graph_builder.add_edge("call_tools", "call_model")

# --- 6. Compile and Run the Agent ---
agent_graph = graph_builder.compile()

if __name__ == "__main__":
    query = "How many words are in the text 'I am a skilled AI engineer'?"

    # The input to the graph is the initial state.
    initial_state = {"messages": [HumanMessage(content=query)], "tool_calls": []}

    print(f"Human: {query}\n")

    # .stream() lets us see the output of each node as it executes.
    for event in agent_graph.stream(initial_state):
        for key, value in event.items():
            print(f"--- Event: {key} ---")
            print(value)
            print("--------------------")

    # .invoke() runs the graph to completion and gives the final state.
    final_state = agent_graph.invoke(initial_state)
    final_answer = final_state["messages"][-1].content

    print("\n--- Agent's Final Answer ---")
    print(final_answer)
