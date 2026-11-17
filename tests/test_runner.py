from src.rag.chatbot import ask_bot
from src.evaluation.runner import run_test_cases


def mock_application(question):
    return {
        "answer": f"Mock response for: {question}",
        "retrieval_context": []
    }


def test_runner_executes_multiple_test_cases():

    test_cases = [
        {
            "id": "TEST001",
            "question": "What is the ATM limit?"
        },
        {
            "id": "TEST002",
            "question": "What is the UPI limit?"
        }
    ]

    results = run_test_cases(
        test_cases=test_cases,
        application=mock_application
    )

    assert len(results) == 2
    assert results[0]["test_id"] == "TEST001"
    assert results[1]["test_id"] == "TEST002"
    assert results[0]["status"] == "executed"
    assert results[1]["status"] == "executed"

def test_runner_with_real_chatbot():

    test_cases = [
        {
            "id": "REAL001",
            "question": "What is the daily ATM withdrawal limit?"
        }
    ]

    results = run_test_cases(
        test_cases=test_cases,
        application=ask_bot
    )

    assert len(results) == 1
    assert results[0]["status"] == "executed"
    assert results[0]["actual_answer"] is not None
    assert len(results[0]["retrieval_context"]) > 0