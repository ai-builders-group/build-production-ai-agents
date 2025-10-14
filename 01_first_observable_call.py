# 01_first_observable_call.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# --- 1. Load Environment Variables (The Cornerstone of Security) ---
# This must be the first step to ensure all required keys are loaded before use.
load_dotenv()

# --- 2. Initialize the Language Model Client (The Universal Adapter) ---
# We initialize our primary client for interacting with LLMs.
llm = ChatOpenAI(
    # We point the client to the OpenRouter gateway.
    base_url="https://openrouter.ai/api/v1",
    # The API key is loaded securely from the environment.
    api_key=os.getenv("OPENROUTER_API_KEY"),
    # We explicitly select our professional workhorse model.
    #     model="google/gemini-2.5-flash",
)


# --- 3. The LLM Invocation (The Core Logic) ---
# This is the core logic where we interact with the LLM.
def get_llm_summary(text_to_summarize: str) -> str:
    """Invokes the LLM to summarize a given text."""

    print("Requesting summary from our Gemini model via OpenRouter...")
    try:
        # The .invoke() method sends the request to the LLM.
        response = llm.invoke(text_to_summarize)
        # The summary text is in the `content` attribute of the response.
        return response.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# --- 4. Run the Script (The Test Case) ---
if __name__ == "__main__":
    # The abstract from the famous "Attention Is All You Need" paper.
    transformer_abstract = """
    The dominant sequence transduction models are based on complex recurrent or
    convolutional neural networks, including an encoder and a decoder. The best
    performing models also connect the encoder and decoder through an attention
    mechanism. We propose a new simple network architecture, the Transformer,
    based solely on attention mechanisms, dispensing with recurrence and convolutions
    entirely. Experiments on two machine translation tasks show these models to
    be superior in quality while being more parallelizable and requiring significantly
    less time to train.
    """

    ai_summary = get_llm_summary(transformer_abstract)

    if ai_summary:
        print("\n--- AI-Generated Summary (Gemini 2.5 Flash) ---")
        print(ai_summary)
