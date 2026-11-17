
import json
from pathlib import Path
from datetime import datetime


def generate_reports(
    quality_results,
    security_results,
    scores,
    reports_dir
):
    """
    Generate JSON and Markdown evaluation reports.
    """

    reports_dir = Path(reports_dir)
    reports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Complete evaluation data
    report_data = {
        "project": "LLM-EvalSuite",
        "generated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "scores": scores,
        "functional_results": quality_results,
        "security_results": security_results
    }

    # ======================================
    # JSON REPORT
    # ======================================

    json_path = reports_dir / "quality_results.json"

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    # ======================================
    # MARKDOWN REPORT
    # ======================================

    functional = scores["functional"]
    quality = scores["quality"]
    security = scores["security"]

    summary = f"""# LLM-EvalSuite Evaluation Report

**Generated:** {report_data["generated_at"]}

## 1. Functional Evaluation

| Metric | Result |
|---|---:|
| Total test cases | {functional["total"]} |
| Passed | {functional["passed"]} |
| Failed | {functional["failed"]} |
| Review required | {functional["review"]} |
| Pass rate | {functional["pass_rate"]}% |

### Functional Status

- PASS: {functional["status_counts"]["PASS"]}
- FAIL: {functional["status_counts"]["FAIL"]}
- REVIEW: {functional["status_counts"]["REVIEW"]}

## 2. Quality Metrics

| Metric | Average Score |
|---|---:|
| Faithfulness | {quality["average_faithfulness"]} |
| Answer Relevancy | {quality["average_answer_relevancy"]} |

- Faithfulness evaluations completed: {quality["faithfulness_evaluated"]}
- Answer relevancy evaluations completed: {quality["relevancy_evaluated"]}

## 3. Security Evaluation

| Metric | Result |
|---|---:|
| Total security tests | {security["total"]} |
| Passed | {security["passed"]} |
| Failed | {security["failed"]} |
| Review required | {security["review"]} |
| Pass rate | {security["pass_rate"]}% |

### Security Status

- PASS: {security["status_counts"]["PASS"]}
- FAIL: {security["status_counts"]["FAIL"]}
- REVIEW: {security["status_counts"]["REVIEW"]}

## 4. Evaluation Overview

Functional tests: {functional["passed"]}/{functional["total"]} passed.

Security tests: {security["passed"]}/{security["total"]} passed.

Incomplete evaluations and cases marked for manual review
are reported separately from confirmed failures.

## 5. Functional Test Details

| Test ID | Category | Status |
|---|---|---|
"""

    for result in quality_results:

        summary += (
            f'| {result.get("id", "N/A")} '
            f'| {result.get("category", "N/A")} '
            f'| {result.get("evaluation_status", "REVIEW")} |\\n'
        )

    summary += """
## 6. Security Test Details

| Test ID | Category | Status |
|---|---|---|
"""

    for result in security_results:

        summary += (
            f'| {result.get("id", "N/A")} '
            f'| {result.get("category", "N/A")} '
            f'| {result.get("evaluation_status", "REVIEW")} |\\n'
        )

    markdown_path = reports_dir / "results_summary.md"

    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(summary)

    print("\\nEvaluation reports generated successfully.")

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
