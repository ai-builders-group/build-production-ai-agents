# tools/retriever_tool.py

import os
from pathlib import Path
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

# --- 1. Security Sandbox Configuration ---
# This block defines the "jail" or "sandbox" for our tool. It calculates
# the absolute path to the project's 'source_code' directory. Any attempt
# by the tool to access files outside this directory will be blocked.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_DIRECTORY = PROJECT_ROOT / "source_code"
VECTORSTORE_PATH = PROJECT_ROOT / "vectorstore"


# --- 2. Tool Input Schema ---
# Defines the expected input for our tool using Pydantic. This provides
# clear validation, typing, and documentation for the tool's interface.
class RetrieverInput(BaseModel):
    query: str = Field(description="The query to search for in the codebase.")


# --- 3. Tool Implementation: The Resilient Retriever ---
@tool("codebase-retriever", args_schema=RetrieverInput)
def codebase_retriever(query: str) -> str:
    """
    Searches the codebase to find relevant code snippets based on the query.
    This tool is hardened with three professional patterns:
    1. Lazy Loading: Loads the vectorstore only when needed.
    2. Sandboxing: Validates file paths to prevent unauthorized access.
    3. Graceful Failure: Handles errors without crashing the agent.
    """
    try:
        # --- 3A. Lazy Loading the Vectorstore ---
        # The expensive I/O operation to load the vectorstore happens here, inside
        # the tool call. This ensures the main application starts instantly.
        print("\n--- Lazily loading vectorstore... ---")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        db = FAISS.load_local(
            str(VECTORSTORE_PATH), embeddings, allow_dangerous_deserialization=True
        )
        retriever = db.as_retriever()
        print("--- Vectorstore loaded successfully. ---")

        retrieved_docs = retriever.invoke(query)

        # --- 3B. Process and Securely Validate Each Document ---
        formatted_docs = []
        for i, doc in enumerate(retrieved_docs):
            source_path_str = doc.metadata.get("source", "Unknown")

            # The SANDBOX VALIDATION logic from Lesson 7 remains.
            try:
                resolved_path = Path(source_path_str).resolve()
                if not resolved_path.is_relative_to(ALLOWED_DIRECTORY):
                    print(
                        f"⚠️ SECURITY WARNING: Attempted to access restricted path: {source_path_str}"
                    )
                    formatted_docs.append(
                        f"--- ACCESS DENIED: Cannot display content from restricted path: {source_path_str} ---"
                    )
                    continue
            except Exception:
                print(
                    f"⚠️ SECURITY WARNING: Invalid source path encountered: {source_path_str}"
                )
                formatted_docs.append(f"--- ACCESS DENIED: Invalid source path ---")
                continue

            formatted_docs.append(
                f"--- Code Snippet {i + 1} (Source: {source_path_str}) ---\n{doc.page_content}"
            )

        if not formatted_docs:
            return "No relevant and accessible code snippets found in the 'source_code' directory."

        return "\n\n".join(formatted_docs)

    except Exception as e:
        # --- 3C. Graceful Failure Handling ---
        # If any part of the process fails (e.g., the vectorstore doesn't exist),
        # this block prevents the entire agent from crashing and provides a
        # helpful error message. This is a key resiliency pattern.
        print(f"--- Error during vectorstore load or retrieval: {e} ---")
        return "Error: Could not access the codebase vectorstore. It may not have been created yet. Please run the indexing script."
