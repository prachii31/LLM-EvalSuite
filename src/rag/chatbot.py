
from src.retrieval.retriever import retrieve_documents
from src.rag.llm_client import generate
from src.rag.prompt_template import build_prompt
from config.config import TOP_K


def is_personalized_investment_request(question):
    """Identify requests for personalized investment advice."""

    question_lower = question.lower()

    investment_phrases = [
        "which stocks should i buy",
        "what stocks should i buy",
        "which shares should i buy",
        "where should i invest",
        "how should i invest",
        "invest my money",
        "personalized investment advice",
        "make maximum profit",
        "maximize my investment returns"
    ]

    return any(
        phrase in question_lower
        for phrase in investment_phrases
    )


def ask_bot(question):

    # Apply deterministic financial safety boundary
    if is_personalized_investment_request(question):

        return {
            "question": question,
            "answer": (
                "I cannot provide personalized investment advice. "
                "Please consult a qualified financial advisor."
            ),
            "retrieval_context": []
        }

    # Retrieve relevant policy documents
    documents = retrieve_documents(
        question,
        k=TOP_K
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Generate chatbot response
    prompt = build_prompt(
        context=context,
        question=question
    )

    answer = generate(prompt)

    return {
        "question": question,
        "answer": answer,
        "retrieval_context": [
            {
                "content": document.page_content,
                "metadata": document.metadata
            }
            for document in documents
        ]
    }
