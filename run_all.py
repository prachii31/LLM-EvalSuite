
import json

from config.config import (
    DATASETS_PATH,
    REPORTS_PATH,
    FAITHFULNESS_THRESHOLD,
    ANSWER_RELEVANCY_THRESHOLD
)

from src.rag.chatbot import ask_bot
from src.evaluation.runner import run_test_cases
from src.evaluation.quality_evaluator import evaluate_quality
from src.evaluation.llm_judge import evaluate_response
from src.evaluation.scoring import calculate_scores
from src.evaluation.report_generator import generate_reports


def load_dataset(filename):
    """Load a JSON test dataset."""

    file_path = DATASETS_PATH / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
MANUAL_REVIEW_IDS = {
    "QA003",
    "QA008",
    "QA009",
    "QA011",
    "QA017"
}

def run_functional_evaluation():
    """Run golden dataset and evaluate answer quality."""

    print("\nStarting functional evaluation...")

    test_cases = load_dataset("golden_dataset.json")

    # Execute questions against the chatbot
    execution_results = run_test_cases(test_cases, ask_bot)

    quality_results = []

    for test_case, result in zip(test_cases, execution_results):

        quality = {
            "faithfulness": {"score": None, "reason": "Not evaluated"},
            "answer_relevancy": {"score": None, "reason": "Not evaluated"}
        }

        if result["status"] == "executed":
            quality = evaluate_quality(
                question=result["question"],
                actual_answer=result["actual_answer"],
                retrieval_context=result["retrieval_context"]
            )

        quality_results.append({
    "id": test_case["id"],
    "category": test_case["category"],
    "question": result["question"],
    "expected_answer": test_case["expected_answer"],
    "actual_answer": result["actual_answer"],
    "retrieval_context": result["retrieval_context"],
    "status": result["status"],
    "error": result["error"],
    "quality": quality,

    "review_required": (
        test_case["id"] in MANUAL_REVIEW_IDS
    )
})

    return quality_results


def run_security_evaluation():
    """Run security tests against the chatbot."""

    print("\nStarting security evaluation...")

    test_cases = load_dataset("security_tests.json")

    security_results = []

    for test_case in test_cases:

        try:
            chatbot_result = ask_bot(test_case["question"])
            actual_answer = chatbot_result["answer"]

            policy_context = "\n\n".join(
                item["content"]
                for item in chatbot_result["retrieval_context"]
            )

            judge_result = evaluate_response(
                question=test_case["question"],
                actual_answer=actual_answer,
                expected_behavior=test_case["reason"],
                policy_context=policy_context
            )

            verdict = judge_result["verdict"]
            reason = judge_result["reason"]

        except Exception as error:
            actual_answer = None
            verdict = "ERROR"
            reason = str(error)

        security_results.append({
            "id": test_case["id"],
            "category": test_case["category"],
            "question": test_case["question"],
            "expected_behavior": test_case["expected_behavior"],
            "expected_reason": test_case["reason"],
            "actual_answer": actual_answer,
            "verdict": verdict,
            "reason": reason
        })

    return security_results


def main():
    print("=" * 50)
    print("          LLM-EvalSuite")
    print("      Chatbot Quality Evaluation")
    print("=" * 50)

    quality_results = run_functional_evaluation()
    security_results = run_security_evaluation()

    scores = calculate_scores(
        quality_results=quality_results,
        security_results=security_results,
        faithfulness_threshold=FAITHFULNESS_THRESHOLD,
        relevancy_threshold=ANSWER_RELEVANCY_THRESHOLD
    )

    generate_reports(
        quality_results=quality_results,
        security_results=security_results,
        scores=scores,
        reports_dir=REPORTS_PATH
    )

    print("\nEvaluation completed.")
    print("\nFunctional pass rate:",
          scores["functional"]["pass_rate"], "%")
    print("Average faithfulness:",
          scores["quality"]["average_faithfulness"])
    print("Average answer relevancy:",
          scores["quality"]["average_answer_relevancy"])
    print("Security pass rate:",
          scores["security"]["pass_rate"], "%")


if __name__ == "__main__":
    main()
