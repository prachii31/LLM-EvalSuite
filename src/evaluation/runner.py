
def run_test_cases(test_cases, application):
    """
    Execute test cases against an LLM application
    and collect the responses.
    """

    results = []

    for test_case in test_cases:

        question = test_case["question"]

        try:
            response = application(question)

            results.append({
                "test_id": test_case["id"],
                "question": question,
                "actual_answer": response["answer"],
                "retrieval_context": response.get(
                    "retrieval_context", []
                ),
                "status": "executed",
                "error": None
            })

        except Exception as error:

            results.append({
                "test_id": test_case["id"],
                "question": question,
                "actual_answer": None,
                "retrieval_context": [],
                "status": "error",
                "error": str(error)
            })

    return results
