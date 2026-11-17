
import json
from pathlib import Path

import pytest

from src.rag.chatbot import ask_bot
from src.evaluation.llm_judge import evaluate_response


# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Locate the security dataset
SECURITY_DATASET_PATH = (
    PROJECT_ROOT / "datasets" / "security_tests.json"
)

# Load security test cases
with open(SECURITY_DATASET_PATH, "r", encoding="utf-8") as file:
    security_tests = json.load(file)


# Run one test for each security scenario
@pytest.mark.parametrize(
    "test_case",
    security_tests,
    ids=[test_case["id"] for test_case in security_tests]
)
def test_security_behavior(test_case):

    # Step 1: Get the customer question
    question = test_case["question"]

    # Step 2: Send the question to Nivara Bank chatbot
    chatbot_result = ask_bot(question)

    # Step 3: Extract the chatbot's answer
    actual_answer = chatbot_result["answer"]

    # Step 4: Extract retrieved policy documents
    policy_context = "\n\n".join(
        item["content"]
        for item in chatbot_result["retrieval_context"]
    )

    # Step 5: Ask the LLM judge to evaluate the response
    judge_result = evaluate_response(
        question=question,
        actual_answer=actual_answer,
        expected_behavior=test_case["reason"],
        policy_context=policy_context
    )

    # Step 6: Display evaluation details
    print("\nSecurity Test:", test_case["id"])
    print("Chatbot Answer:", actual_answer)
    print("Policy Context:", policy_context)
    print("Judge Verdict:", judge_result["verdict"])
    print("Judge Reason:", judge_result["reason"])

    # Step 7: Mark the test as passed or failed
    assert judge_result["verdict"] == "PASS", (
        f"Security test failed: {test_case['id']}\n"
        f"Reason: {judge_result['reason']}\n"
        f"Chatbot Answer: {actual_answer}"
    )
