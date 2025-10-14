# tools/retriever_tool.py

from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

# Define the path to our pre-built knowledge base.
VECTORSTORE_PATH = "./vectorstore"

# --- 1. Eager Loading of the Vectorstore ---
# This block runs *once* when the script is first imported. It loads the
# entire vectorstore from disk into memory, making it instantly available
# for any subsequent tool calls. This is known as "eager loading".
print("--- LOADING VECTORSTORE ---")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
try:
    # We load the FAISS index from the specified path.
    db = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        # This flag is required for loading FAISS indexes with custom embeddings.
        allow_dangerous_deserialization=True,
    )
    # The .as_retriever() method creates a standardized interface for searching.
    retriever = db.as_retriever()
    print("--- VECTORSTORE LOADED SUCCESSFULLY ---")
except Exception as e:
    # If loading fails, we set the retriever to None to handle the error gracefully.
    print(f"--- FAILED TO LOAD VECTORSTORE: {e} ---")
    retriever = None


# --- 2. Define the Tool's Input Schema ---
# We use Pydantic to define a clear, machine-readable schema for the tool's
# input. The 'description' field is crucial, as it's what the LLM reads
# to understand what information to provide for the 'query' argument.
class RetrieverInput(BaseModel):
    query: str = Field(description="The query to search for in the codebase.")


# --- 3. Create the Tool Implementation ---
@tool("codebase-retriever", args_schema=RetrieverInput)
def codebase_retriever(query: str) -> str:
    """
    Searches the codebase to find relevant code snippets based on the query.
    Returns the retrieved code snippets as a formatted string.
    """
    # This is a guard clause. If the vectorstore failed to load, the tool
    # will return a helpful error message instead of crashing.
    if retriever is None:
        return "Error: Vectorstore not loaded. Please run the indexing script."

    # The core logic: use the retriever to find documents similar to the query.
    retrieved_docs = retriever.invoke(query)

    # Format the retrieved documents into a clean, readable string. This is
    # what the LLM will see as the tool's output.
    formatted_docs = []
    for i, doc in enumerate(retrieved_docs):
        source = doc.metadata.get("source", "Unknown")
        formatted_docs.append(
            f"--- Code Snippet {i + 1} (Source: {source}) ---\n{doc.page_content}"
        )

    return "\n\n".join(formatted_docs)
