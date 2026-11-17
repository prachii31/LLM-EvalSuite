
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    validate_config
)


def test_embedding_generation():
    validate_config()

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )

    text = "ShopSphere offers free delivery on orders above Rs. 999."

    vector = embeddings.embed_query(text)

    print("\nEmbedding generated successfully!")
    print("Vector dimensions:", len(vector))
    print("First five values:", vector[:5])


if __name__ == "__main__":
    test_embedding_generation()
