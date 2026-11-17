
import json
import pytest

from config.config import (
    FAITHFULNESS_THRESHOLD,
    ANSWER_RELEVANCY_THRESHOLD
)
from src.rag.chatbot import ask_bot
from src.evaluation.quality_evaluator import evaluate_quality

ANSWERABLE_CATEGORIES = ("accounts", "cards", "fees", "payments")

with open("datasets/golden_dataset.json", encoding="utf-8") as f:
    dataset = json.load(f)

answerable = [
    q for q in dataset
    if q["category"] in ANSWERABLE_CATEGORIES
]

assert answerable, (
    f"No questions matched {ANSWERABLE_CATEGORIES}. "
    f"Categories in dataset: {sorted({q['category'] for q in dataset})}"
)


@pytest.mark.slow
@pytest.mark.parametrize("item", answerable, ids=lambda i: i["id"])
def test_chatbot_quality(item, quality_results):
    question = item["question"]
    bot = ask_bot(question)

    result = evaluate_quality(
        question=question,
        actual_answer=bot["answer"],
        retrieval_context=bot["retrieval_context"],
    )

    faith = result["faithfulness"]
    rel = result["answer_relevancy"]
    
    print("Faithfulness:", faith)
    print("Answer Relevancy:", rel)

    quality_results.append({
        "id": item["id"],
        "category": item["category"],
        "question": question,
        "answer": bot["answer"],
        "faithfulness": faith["score"],
        "faithfulness_reason": faith.get("reason", ""),
        "relevancy": rel["score"],
        "relevancy_reason": rel.get("reason", ""),
        "retrieval_context": bot["retrieval_context"]
    })

    assert faith["score"] is not None, (
        f"Judge error (faithfulness): {faith['reason']}"
    )
    assert rel["score"] is not None, (
        f"Judge error (relevancy): {rel['reason']}"
    )

    assert faith["score"] >= FAITHFULNESS_THRESHOLD, (
        f"Faithfulness {faith['score']} < {FAITHFULNESS_THRESHOLD}. "
        f"Answer: {bot['answer']!r}. Judge reason: {faith['reason']}"
    )

    assert rel["score"] >= ANSWER_RELEVANCY_THRESHOLD, (
        f"Relevancy {rel['score']} < {ANSWER_RELEVANCY_THRESHOLD}. "
        f"Answer: {bot['answer']!r}. Judge reason: {rel['reason']}"
    )
