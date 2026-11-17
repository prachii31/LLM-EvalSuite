from src.evaluation.quality_evaluator import evaluate_quality

QUESTION = "What is the daily ATM withdrawal limit for a Basic account?"
CONTEXT = [{"content": "The daily ATM withdrawal limit for a Basic account is ₹40,000."}]


def test_faithful_answer_scores_high():
    r = evaluate_quality(QUESTION,
                         "The daily ATM withdrawal limit for a Basic account is ₹40,000.",
                         CONTEXT)
    assert r["faithfulness"]["score"] is not None, r["faithfulness"]["reason"]
    assert r["faithfulness"]["score"] >= 0.8


def test_hallucinated_answer_scores_low():
    r = evaluate_quality(QUESTION,
                         "The limit is ₹1,00,000, and you also get free airport lounge access.",
                         CONTEXT)
    assert r["faithfulness"]["score"] is not None, r["faithfulness"]["reason"]
    assert r["faithfulness"]["score"] <= 0.5


def test_irrelevant_answer_scores_low():
    r = evaluate_quality(QUESTION,
                         "Nivara Bank was founded to serve customers with care.",
                         CONTEXT)
    assert r["answer_relevancy"]["score"] is not None, r["answer_relevancy"]["reason"]
    assert r["answer_relevancy"]["score"] <= 0.5