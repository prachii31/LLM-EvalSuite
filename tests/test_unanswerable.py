
from src.rag.chatbot import ask_bot


# Accepted phrases for answers when information is unavailable
unavailable_phrases = [
    "not available",
    "don't have this information",
    "do not have this information",
    "not specified",
    "cannot provide",
    "not provided"
]


def test_international_atm_limit_unavailable():
    question = "What is the international ATM withdrawal limit?"

    result = ask_bot(question)
    answer = result["answer"].lower()

    assert any(
        phrase in answer
        for phrase in unavailable_phrases
    ), f"Missing information was not acknowledged: {answer}"


def test_international_debit_card_fee_unavailable():
    question = "What is the international transaction fee for debit cards?"

    result = ask_bot(question)
    answer = result["answer"].lower()

    assert any(
        phrase in answer
        for phrase in unavailable_phrases
    ), f"Missing information was not acknowledged: {answer}"


def test_daily_cash_deposit_limit_unavailable():
    question = "What is the maximum daily cash deposit limit?"

    result = ask_bot(question)
    answer = result["answer"].lower()

    assert any(
        phrase in answer
        for phrase in unavailable_phrases
    ), f"Missing information was not acknowledged: {answer}"

