# 08_resilient_agent.py

import os
import shutil
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# --- 1. Import Components for Testing ---
from agent_graph_factory import build_agent_graph
from tools.retriever_tool import codebase_retriever

# We import both the public tool and its "private" internal function
# so we can directly test the caching decorator.
from tools.structured_analyzer_tool import (
    structured_code_analyzer,
    _analyze_with_retry_and_cache,
)

load_dotenv()
VECTORSTORE_PATH = "./vectorstore"
VECTORSTORE_BACKUP_PATH = "./vectorstore_backup"


# --- 2. Main Demonstration Function ---
def main():
    """Main function to demonstrate the resilient agent's features."""
    print("--- Resilient Agent Demonstration ---")

    # --- SCENARIO 1: DEMONSTRATE GRACEFUL FAILURE ---
    print("\n--- SCENARIO 1: GRACEFUL FAILURE (VECTORSTORE NOT FOUND) ---")

    # Arrange: Temporarily hide the vectorstore to simulate a failure condition.
    if os.path.exists(VECTORSTORE_PATH):
        shutil.move(VECTORSTORE_PATH, VECTORSTORE_BACKUP_PATH)
        print(
            f"Temporarily moved vectorstore to '{VECTORSTORE_BACKUP_PATH}' to simulate failure."
        )

    # Act: Assemble and run the agent.
    tools = [codebase_retriever]
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-flash",
        temperature=0,
    )
    app = build_agent_graph(llm, tools)
    query1 = "What is the purpose of the 'call_model' function?"
    initial_state1 = {"messages": [HumanMessage(content=query1)]}
    print(f"\nHuman: {query1}")
    response1 = app.invoke(initial_state1)

    # Assert: Observe the agent's helpful error message instead of a crash.
    print(f"Agent: {response1['messages'][-1].content}")

    # Cleanup: Restore the vectorstore for the next scenario.
    if os.path.exists(VECTORSTORE_BACKUP_PATH):
        shutil.move(VECTORSTORE_BACKUP_PATH, VECTORSTORE_PATH)
        print(f"\nRestored vectorstore from backup.")

    # --- SCENARIO 2: DEMONSTRATE CACHING ---
    print("\n\n--- SCENARIO 2: CACHING (DIRECT FUNCTION CALL) ---")

    sample_code = "def my_sample_function(a: int, b: int) -> int:\n    return a + b"

    # Act 1: Call the decorated function for the first time.
    print(f"\nFirst call to the internal, decorated function...")
    response2a = _analyze_with_retry_and_cache(sample_code)
    print(f"Result (First Call):\n{response2a}")

    # Act 2: Call it again with the same input.
    print(f"\nSecond call... (Should be cached, no 'Cache miss' message)")
    response2b = _analyze_with_retry_and_cache(sample_code)
    print(f"Result (Second Call):\n{response2b}")


if __name__ == "__main__":
    main()
