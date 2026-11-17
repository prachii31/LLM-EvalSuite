
from src.retrieval.retriever import retrieve_documents


def test_atm_limit_retrieval():
    question = "What is the daily ATM withdrawal limit?"

    documents = retrieve_documents(question)

    assert len(documents) > 0

    retrieved_text = " ".join(
        document.page_content.lower()
        for document in documents
    )

    assert "25,000" in retrieved_text
    assert "atm" in retrieved_text


def test_savings_interest_retrieval():
    question = "What is the interest rate on a regular savings account?"

    documents = retrieve_documents(question)

    assert len(documents) > 0

    retrieved_text = " ".join(
        document.page_content.lower()
        for document in documents
    )

    assert "3%" in retrieved_text
    assert "savings" in retrieved_text


def test_upi_limit_retrieval():
    question = "What is the maximum daily UPI transaction limit?"

    documents = retrieve_documents(question)

    assert len(documents) > 0

    retrieved_text = " ".join(
        document.page_content.lower()
        for document in documents
    )

    assert "1,00,000" in retrieved_text
    assert "upi" in retrieved_text
