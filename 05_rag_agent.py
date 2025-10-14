# 05_rag_agent.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- 1. Import Core Components ---
# We import our reusable graph factory, which encapsulates the logic for
# building the agent's reasoning loop.
from agent_graph_factory import build_agent_graph

# We also import our new, specialized tool that connects the agent to its
# long-term memory (the vectorstore).
from tools.retriever_tool import codebase_retriever

# --- 2. The RAG-Specific System Prompt ---
# This is the most critical part of the RAG agent's architecture. It's not
# just a persona; it's a detailed, step-by-step algorithm that forces the LLM
# to follow a specific research process. This instructional style of prompting
# is key to building reliable, fact-based AI systems.
SYSTEM_PROMPT = """You are a senior AI software engineer and a world-class expert in analyzing source code. You are a master of logic, precision, and following instructions exactly.

Your mission is to answer a user's question about a codebase using a precise, two-step reasoning process.

**STEP 1: Broad Retrieval.**
First, you MUST use the `codebase-retriever` tool to find all potentially relevant code snippets. This is your only way to access the codebase.

**STEP 2: Focused Synthesis & Analysis.**
After retrieving the code, you will analyze the snippets to answer the user's specific question. Your final answer MUST be based SOLELY on the information retrieved.
- If the user asks about a specific function or class, you must find that exact function/class in the retrieved context and explain its purpose, arguments, and logic.
- You will ignore all other retrieved code that is not directly relevant to the user's specific question. Do not summarize all the files you found.
- If the retrieved context does not contain the answer to the question, you must state that you could not find the information in the provided codebase.

You will now begin. The user's question is waiting.
"""

# --- 3. Main Execution Block ---
if __name__ == "__main__":
    load_dotenv()
    print("--- RAG Agent ---")

    # --- 4. Assemble the Agent ---
    llm = ChatOpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-pro",
        temperature=0,
    )

    # Principle of Least Confusion: We give the agent ONLY the tool it needs
    # for its core mission. This prevents distraction and increases reliability.
    tools = [codebase_retriever]

    # We use our factory to cleanly assemble the agent.
    agent_graph = build_agent_graph(llm, tools)

    # --- 5. Define the Query and Initial State ---
    # This query is a specific, knowledge-based question that a generic LLM
    # could not answer. It requires the agent to perform research.
    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content="How does the 'call_model' node in this project work?"
            ),
        ]
    }
    print(f"Human: {initial_state['messages'][-1].content}\n")

    # --- 6. Execute the Agent and Display the Result ---
    final_state = agent_graph.invoke(initial_state)
    final_answer = final_state["messages"][-1].content

    print("\n--- Agent's Final Answer ---")
    print(final_answer)
