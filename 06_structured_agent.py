# 06_structured_agent.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# --- 1. Import Core Components ---
# We import our reusable graph factory and the Pydantic schema that defines
# the desired structured output for our analysis.
from agent_graph_factory import build_agent_graph
from schemas.function_analysis import FunctionAnalysis

# We also import all available tools for the agent to use.
from tools.retriever_tool import codebase_retriever
from tools.structured_analyzer_tool import structured_code_analyzer

# --- 2. Define the System Prompt for Tool Chaining ---
# This prompt is a direct, step-by-step instruction. It guides the agent
# on how to chain its tools: first retrieve context, then perform analysis.
SYSTEM_PROMPT = """You are an expert AI software engineer. Your job is to answer a user's question by chaining tools.
First, use the `codebase-retriever` to find the relevant code.
Then, if the user asks for a structured analysis, use the `structured-code-analyzer` on the retrieved code.
The direct output of the final tool is your answer."""

# --- 3. Main Execution Block ---
if __name__ == "__main__":
    load_dotenv()
    print("--- Multi-Tool Router Agent ---")

    # --- 4. Assemble the Agent's Components ---
    # A powerful model is required for effective multi-step reasoning and tool selection.
    llm = ChatOpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-pro",
        temperature=0,
    )
    # The agent is now given access to *two* distinct tools.
    tools = [codebase_retriever, structured_code_analyzer]
    agent_graph = build_agent_graph(llm, tools)

    # --- 5. Define the Trigger Query ---
    # This query is specifically crafted to trigger the full tool chain. The phrase
    # "structured analysis" is a key signal for the agent to use the second tool.
    query = "Please provide a structured analysis of the 'call_model' function from the state machine lesson."
    initial_state = {
        "messages": [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=query)]
    }
    print(f"Human: {query}\n")

    # --- 6. Execute the Agent and Parse the Final Answer ---
    final_state = agent_graph.invoke(initial_state)

    # This is a resilient parsing pattern. Instead of trusting the agent's final
    # chatty message, we search backwards through the message history to find the
    # *actual raw output from the tool*. This is the "ground truth."
    print("\n--- Agent's Final Answer (Ground Truth from Tool) ---")
    final_answer = final_state["messages"][-1].content
    for message in reversed(final_state["messages"]):
        if (
            isinstance(message, ToolMessage)
            and message.name == "structured-code-analyzer"
        ):
            # The content of this ToolMessage is the direct, structured output
            # we need, free of any conversational fluff from the LLM.
            final_answer = message.content
            break

    # We print the direct, raw output. In a real application, this string
    # would be parsed back into a Pydantic object for further processing.
    print(final_answer)
