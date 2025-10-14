# 02_agent_state_machine.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# --- 1. Load Environment Variables ---
load_dotenv()


# --- 2. Define the Agent's State (Its Memory) ---
class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]


# --- 3. Define the Nodes (The "Workers") ---
def call_model(state: AgentState):
    """A node that calls the LLM to generate a response."""
    print("---CALLING THE MODEL---")
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-flash",
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# --- 4. Define the Graph (The Agent's "Brain" Structure) ---
graph_builder = StateGraph(AgentState)
graph_builder.add_node("call_model", call_model)
graph_builder.set_entry_point("call_model")
graph_builder.add_edge("call_model", END)

# --- 5. Compile the Graph into a Runnable ---
agent_graph = graph_builder.compile()

# --- 6. Run the Agent in a Conversational Loop ---
if __name__ == "__main__":
    print("Hello! I am your AI assistant. How can I help you today?")
    print("Type 'exit' to end the conversation.")

    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        messages.append(HumanMessage(content=user_input))
        response = agent_graph.invoke({"messages": messages})
        messages = response["messages"]
        ai_message = messages[-1].content
        print(f"AI: {ai_message}")
