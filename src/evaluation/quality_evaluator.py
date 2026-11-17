

import json
import hashlib
from pathlib import Path

from deepeval.models import OllamaModel
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric
)
from deepeval.test_case import LLMTestCase


# ==========================================
# EVALUATION CONFIGURATION
# ==========================================

JUDGE_MODEL_NAME = "qwen2.5:7b"
JUDGE_BASE_URL = "http://localhost:11434"

FAITHFULNESS_THRESHOLD = 0.7
ANSWER_RELEVANCY_THRESHOLD = 0.7

# Increase this version whenever evaluation logic changes.
EVALUATOR_VERSION = "2"


# ==========================================
# LOCAL JUDGE MODEL
# ==========================================

judge_model = OllamaModel(
    model=JUDGE_MODEL_NAME,
    base_url=JUDGE_BASE_URL,
    temperature=0
)


# ==========================================
# DEEPEVAL METRICS
# ==========================================

faithfulness_metric = FaithfulnessMetric(
    model=judge_model,
    threshold=FAITHFULNESS_THRESHOLD,
    async_mode=False
)

relevancy_metric = AnswerRelevancyMetric(
    model=judge_model,
    threshold=ANSWER_RELEVANCY_THRESHOLD,
    async_mode=False
)


# ==========================================
# CACHE CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CACHE_FILE = (
    PROJECT_ROOT
    / "cache"
    / "deepeval_quality_cache.json"
)


def load_cache():
    """Load previously evaluated results."""

    CACHE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if CACHE_FILE.exists():

        try:
            with open(
                CACHE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                cache = json.load(file)

                if isinstance(cache, dict):
                    return cache

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not load evaluation cache.")

    return {}


def save_cache(cache):
    """Save evaluation results."""

    CACHE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cache,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# CACHE KEY GENERATION
# ==========================================

def create_cache_key(question, answer, context):
    """Generate a unique, versioned evaluation cache key."""

    content = json.dumps(
        {
            "evaluator_version": EVALUATOR_VERSION,
            "model": JUDGE_MODEL_NAME,
            "faithfulness_threshold": FAITHFULNESS_THRESHOLD,
            "answer_relevancy_threshold": ANSWER_RELEVANCY_THRESHOLD,
            "question": question,
            "answer": answer,
            "context": context
        },
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


# ==========================================
# CONTEXT NORMALIZATION
# ==========================================

def normalize_context(retrieval_context):
    """Convert retrieved documents into text for DeepEval."""

    context = []

    for item in retrieval_context:

        if isinstance(item, dict):

            content = item.get("content", "")

        else:

            content = str(item)

        if content:
            context.append(str(content))

    return context


# ==========================================
# INDIVIDUAL METRIC EVALUATION
# ==========================================

def evaluate_faithfulness(test_case):
    """Evaluate whether the answer is supported by retrieved context."""

    try:

        faithfulness_metric.measure(test_case)

        return {
            "score": float(faithfulness_metric.score),
            "reason": faithfulness_metric.reason
        }

    except Exception as error:

        return {
            "score": None,
            "reason": f"Evaluation error: {error}"
        }


def evaluate_relevancy(test_case):
    """Evaluate whether the answer addresses the question."""

    try:

        relevancy_metric.measure(test_case)

        return {
            "score": float(relevancy_metric.score),
            "reason": relevancy_metric.reason
        }

    except Exception as error:

        return {
            "score": None,
            "reason": f"Evaluation error: {error}"
        }


# ==========================================
# MAIN QUALITY EVALUATION
# ==========================================

def evaluate_quality(
    question,
    actual_answer,
    retrieval_context
):
    """
    Evaluate chatbot output using DeepEval.

    Metrics:
    1. Faithfulness
    2. Answer Relevancy

    Uses local Ollama judge model and persistent caching.
    """

    context = normalize_context(retrieval_context)

    cache = load_cache()

    cache_key = create_cache_key(
        question,
        actual_answer,
        context
    )

    # Check cache
    if cache_key in cache:

        cached_result = cache[cache_key]

        if (
            isinstance(cached_result, dict)
            and cached_result.get("faithfulness", {}).get("score") is not None
            and cached_result.get("answer_relevancy", {}).get("score") is not None
        ):

            print("Using cached DeepEval results.")

            return cached_result

    print("Running DeepEval evaluation...")

    test_case = LLMTestCase(
        input=question,
        actual_output=actual_answer,
        retrieval_context=context
    )

    # Evaluate both metrics independently
    faithfulness_result = evaluate_faithfulness(
        test_case
    )

    print(
        "Faithfulness:",
        faithfulness_result
    )

    relevancy_result = evaluate_relevancy(
        test_case
    )

    print(
        "Answer Relevancy:",
        relevancy_result
    )

    results = {
        "faithfulness": faithfulness_result,
        "answer_relevancy": relevancy_result
    }

    # Cache only when both metrics return valid scores
    if (
        results["faithfulness"]["score"] is not None
        and results["answer_relevancy"]["score"] is not None
    ):

        cache[cache_key] = results

        save_cache(cache)

        print("Evaluation results cached.")

    else:

        print(
            "Evaluation was incomplete. "
            "Results were not cached."
        )

    return results
