# 04_create_vectorstore.py

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

SOURCE_CODE_PATH = "./source_code"
VECTORSTORE_PATH = "./vectorstore"


def main():
    """
    This script creates a FAISS vectorstore from the source code documents.
    It follows the Load -> Split -> Embed -> Store pipeline.
    """
    print("--- Starting Vectorstore Creation ---")

    # --- 1. LOAD ---
    # Use a DirectoryLoader to ingest all .py files.
    print(f"Loading documents from {SOURCE_CODE_PATH}...")
    loader = DirectoryLoader(
        SOURCE_CODE_PATH,
        glob="**/*.py",  # Load only Python files
        loader_cls=TextLoader,  # Use TextLoader for .py files
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s).")

    # --- 2. SPLIT ---
    # Use a RecursiveCharacterTextSplitter for intelligent chunking.
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    # --- 3. EMBED ---
    # Select a high-quality, open-source embedding model that runs locally.
    print("Initializing embedding model...")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # --- 4. STORE ---
    # Create the FAISS vectorstore from the chunks and embeddings.
    print("Creating FAISS vectorstore...")
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(VECTORSTORE_PATH)

    print("--- Vectorstore Creation Complete ---")
    print(f"Vectorstore saved at: {VECTORSTORE_PATH}")


if __name__ == "__main__":
    main()
