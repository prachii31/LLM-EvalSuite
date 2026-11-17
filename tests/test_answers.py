
from src.rag.chatbot import ask_bot


def test_atm_limit_answer():

    question = "What is the daily ATM withdrawal limit?"

    result = ask_bot(question)

    answer = result["answer"].lower()

    assert "25,000" in answer
    assert "atm" in answer



def test_premium_savings_interest_answer():

    question = "What is the interest rate on a Premium Savings Account?"

    result = ask_bot(question)

    answer = result["answer"].lower()

    assert "3.5%" in answer
    assert "interest" in answer


def test_upi_limit_answer():

    question = "What is the maximum daily UPI transaction limit?"

    result = ask_bot(question)

    answer = result["answer"].lower()

    assert "1,00,000" in answer
    assert "upi" in answer
