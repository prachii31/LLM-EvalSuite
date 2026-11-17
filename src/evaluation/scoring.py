
def calculate_scores(
    quality_results,
    security_results,
    faithfulness_threshold=0.7,
    relevancy_threshold=0.7
):
    """
    Calculate functional, quality and security scores.

    Functional outcomes:
    PASS   - Both metrics meet their thresholds.
    FAIL   - Both metrics have valid scores, but one or both
             are below threshold.
    REVIEW - A metric failed to execute or the result requires
             manual review.
    """

    total_quality = len(quality_results)
    total_security = len(security_results)

    faithfulness_scores = []
    relevancy_scores = []

    functional_counts = {
        "PASS": 0,
        "FAIL": 0,
        "REVIEW": 0
    }

    security_counts = {
        "PASS": 0,
        "FAIL": 0,
        "REVIEW": 0,
        "ERROR": 0
    }

    for result in quality_results:

        quality = result.get("quality", {})

        faith = quality.get("faithfulness", {})
        relevancy = quality.get("answer_relevancy", {})

        faithfulness = faith.get("score")
        relevancy_score = relevancy.get("score")

        # Keep only valid numerical scores
        if faithfulness is not None:
            faithfulness_scores.append(float(faithfulness))

        if relevancy_score is not None:
            relevancy_scores.append(float(relevancy_score))

        # Allow explicit manual review marking
        if result.get("review_required", False):
            status = "REVIEW"

        # Incomplete evaluation requires review
        elif faithfulness is None or relevancy_score is None:
            status = "REVIEW"

        # Both metrics pass
        elif (
            faithfulness >= faithfulness_threshold
            and relevancy_score >= relevancy_threshold
        ):
            status = "PASS"

        # Valid evaluation, but below threshold
        else:
            status = "FAIL"

        result["evaluation_status"] = status
        functional_counts[status] += 1

    # Security evaluation
    for result in security_results:

        verdict = result.get("verdict", "ERROR").upper()

        if verdict == "PASS":
            status = "PASS"

        elif verdict == "FAIL":
            status = "FAIL"

        else:
            status = "REVIEW"

        result["evaluation_status"] = status

        if status in security_counts:
            security_counts[status] += 1

    # Average quality scores
    average_faithfulness = (
        sum(faithfulness_scores) / len(faithfulness_scores)
        if faithfulness_scores else 0
    )

    average_relevancy = (
        sum(relevancy_scores) / len(relevancy_scores)
        if relevancy_scores else 0
    )

    functional_passed = functional_counts["PASS"]
    functional_failed = functional_counts["FAIL"]
    functional_review = functional_counts["REVIEW"]

    security_passed = security_counts["PASS"]
    security_failed = security_counts["FAIL"]
    security_review = security_counts["REVIEW"]

    return {
        "functional": {
            "total": total_quality,
            "passed": functional_passed,
            "failed": functional_failed,
            "review": functional_review,
            "pass_rate": round(
                functional_passed / total_quality * 100, 2
            ) if total_quality else 0,
            "status_counts": functional_counts
        },

        "quality": {
            "average_faithfulness": round(
                average_faithfulness, 2
            ),
            "average_answer_relevancy": round(
                average_relevancy, 2
            ),
            "faithfulness_evaluated": len(faithfulness_scores),
            "relevancy_evaluated": len(relevancy_scores)
        },

        "security": {
            "total": total_security,
            "passed": security_passed,
            "failed": security_failed,
            "review": security_review,
            "pass_rate": round(
                security_passed / total_security * 100, 2
            ) if total_security else 0,
            "status_counts": security_counts
        }
    }
