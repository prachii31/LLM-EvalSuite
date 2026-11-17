
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from config.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    KNOWLEDGE_BASE_PATH,
    CHROMA_PATH,
    validate_config
)


COLLECTION_NAME = "nivara_bank_policies"


def load_documents():

    print("Loading Nivara Bank policy documents...")

    documents = []

    # Find all text files in the raw documents folder
    file_paths = sorted(KNOWLEDGE_BASE_PATH.glob("*.txt"))

    if not file_paths:
        raise FileNotFoundError(
            f"No policy documents found in: {KNOWLEDGE_BASE_PATH}"
        )

    # Read each policy document
    for file_path in file_paths:

        text = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "bank": "Nivara Bank"
            }
        )

        documents.append(document)

        print(f"Loaded: {file_path.name}")

    print(f"\nTotal documents loaded: {len(documents)}")

    return documents


def split_documents(documents):

    print("\nSplitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    return chunks


def store_documents(chunks):

    if not chunks:
        raise ValueError("No document chunks available to store.")

    print("\nInitializing Gemini embeddings...")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )

    print("Connecting to ChromaDB...")

    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    # Open the existing collection, if it exists
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    # Remove old records before rebuilding the collection
    vector_store.delete_collection()

    # Create a fresh collection
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    # Generate unique IDs for every document chunk
    ids = [
        f"{chunk.metadata['source']}_{index}"
        for index, chunk in enumerate(chunks)
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=ids
    )

    print(f"Successfully stored {len(chunks)} chunks in ChromaDB!")


def run_ingestion():

    validate_config()

    documents = load_documents()

    chunks = split_documents(documents)

    store_documents(chunks)

    print("\nNivara Bank document ingestion completed successfully!")


if __name__ == "__main__":
    run_ingestion()
