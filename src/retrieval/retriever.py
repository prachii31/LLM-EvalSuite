
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from config.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    TOP_K,
    validate_config
)


COLLECTION_NAME = "nivara_bank_policies"


def get_vector_store():

    validate_config()

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    return vector_store


def retrieve_documents(question, k=TOP_K):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results


if __name__ == "__main__":

    question = "What is the daily ATM withdrawal limit?"

    documents = retrieve_documents(question)

    print("\nCustomer Question:", question)
    print("\nRetrieved Nivara Bank policy documents:")

    for document in documents:

        print("\nContent:", document.page_content)
        print("Metadata:", document.metadata)
