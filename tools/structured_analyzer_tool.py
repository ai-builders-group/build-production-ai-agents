# tools/structured_analyzer_tool.py

import os
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from schemas.function_analysis import FunctionAnalysis

# --- 1. Import Resilience Decorators ---
# `lru_cache` provides in-memory caching for function calls.
# `tenacity` provides a powerful `@retry` decorator for handling transient errors.
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential


# --- 2. Tool Input Schema ---
class AnalyzerToolInput(BaseModel):
    code_snippet: str = Field(
        description="A string containing a single, complete Python function to be analyzed."
    )


# --- 3. The Public Interface ---
# This is the clean, public-facing function that LangChain's @tool decorator
# can easily inspect to understand its signature and purpose. Its only job
# is to delegate the actual work to our decorated internal function.
@tool("structured-code-analyzer", args_schema=AnalyzerToolInput)
def structured_code_analyzer(code_snippet: str) -> FunctionAnalysis:
    """
    Analyzes a Python function's code snippet and returns a structured analysis.
    This tool is cached and will retry up to 3 times on network failure.
    Use this when you need a detailed, structured breakdown of a specific function.
    """
    return _analyze_with_retry_and_cache(code_snippet)


# --- 4. The Decorated Internal Implementation ---
# This "private" function contains the core logic. We apply our resilience
# and performance decorators here, hidden from the main @tool decorator.


@lru_cache(maxsize=32)  # Cache up to 32 recent, unique results.
@retry(
    stop=stop_after_attempt(3),  # Retry the function up to 3 times if it fails.
    wait=wait_exponential(
        multiplier=1, min=1, max=10
    ),  # Wait 1s, then 2s, then 4s... between retries.
)
def _analyze_with_retry_and_cache(code_snippet: str) -> FunctionAnalysis:
    """Internal function to perform the analysis with caching and retries."""
    # This print statement is a simple way to prove that our cache is working.
    # It will only appear on a "cache miss" (the first time a unique input is seen).
    print("\n--- Calling structured_code_analyzer (Cache miss or new input) ---")

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="google/gemini-2.5-flash",
        temperature=0,
    )

    structured_llm = llm.with_structured_output(FunctionAnalysis)
    prompt = f"Analyze this Python function and describe its purpose, arguments, and return value. Here is the function: ```python\n{code_snippet}\n```"

    analysis_result = structured_llm.invoke(prompt)
    return analysis_result
