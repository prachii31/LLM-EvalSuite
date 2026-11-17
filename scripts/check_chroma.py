
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    validate_config
)


def test_chroma_database():

    validate_config()

    # Initialize hosted embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )

    # ShopSphere sample knowledge
    documents = [
        Document(
            page_content="ShopSphere offers free delivery on orders above Rs. 999.",
            metadata={"category": "delivery"}
        ),
        Document(
            page_content="Orders below Rs. 999 have a delivery charge of Rs. 50.",
            metadata={"category": "delivery"}
        ),
        Document(
            page_content="Customers can return eligible products within 7 days of delivery.",
            metadata={"category": "returns"}
        ),
        Document(
            page_content="Refunds are processed within 5 to 7 business days after approval.",
            metadata={"category": "refunds"}
        )
    ]

    # Create a persistent ChromaDB collection
    vector_store = Chroma(
        collection_name="shopsphere_test",
        embedding_function=embeddings,
        persist_directory="./storage/chroma"
    )

    # Add documents using stable IDs
    vector_store.add_documents(
        documents=documents,
        ids=["delivery_1", "delivery_2", "returns_1", "refunds_1"]
    )

    print("\nDocuments stored successfully!")

    # Search for relevant information
    query = "Is delivery free for my order?"

    results = vector_store.similarity_search(
        query,
        k=2
    )

    print("\nSearch results:")

    for result in results:
        print("\nContent:", result.page_content)
        print("Category:", result.metadata["category"])


if __name__ == "__main__":
    test_chroma_database()
