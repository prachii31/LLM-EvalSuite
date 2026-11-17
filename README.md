# LLM-EvalSuite
### A Lightweight Framework for RAG Chatbot Quality and Security Evaluation

LLM-EvalSuite is a Python-based framework designed to evaluate the quality, reliability, and security of Large Language Model (LLM) applications.

The project uses **Nivara Bank**, a fictional banking chatbot built using Retrieval-Augmented Generation (RAG), as its application under test.

It combines functional testing, LLM-based quality evaluation, and security testing to assess chatbot responses against predefined test datasets.

The framework uses DeepEval to evaluate response faithfulness and answer relevancy, while a separate LLM judge evaluates security-related behaviour. It generates structured JSON and Markdown reports to summarize evaluation results.

---

## Project Objectives

- Evaluate the correctness of RAG chatbot responses.
- Measure whether generated answers are supported by retrieved context.
- Evaluate the relevance of answers to user questions.
- Test chatbot behaviour against prompt injection and security-related scenarios.
- Identify responses that require manual review.
- Generate automated evaluation reports.

## Key Features

### 1. Functional Testing
- Uses a predefined golden dataset.
- Tests chatbot responses against expected answers and behaviour.
- Captures generated answers and retrieved context.

### 2. Faithfulness Evaluation
- Uses DeepEval's Faithfulness metric.
- Evaluates whether generated answers are supported by the retrieved context.
- Helps identify unsupported or contradictory claims.

### 3. Answer Relevancy Evaluation
- Uses DeepEval's Answer Relevancy metric.
- Evaluates whether chatbot responses address the user's question.

### 4. Security Testing
Tests chatbot behaviour against scenarios involving:
- Prompt injection.
- Sensitive credential disclosure.
- Customer privacy violations.
- Unauthorized transaction claims.
- Unsafe or unsupported financial advice.

### 5. Automated Scoring
- Calculates functional pass rates.
- Calculates average faithfulness and answer relevancy scores.
- Calculates security pass rates.
- Identifies cases requiring manual review.

### 6. Report Generation
Generates:
- JSON reports containing detailed evaluation results.
- Markdown reports containing readable evaluation summaries.

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Document Embeddings | Google Gemini Embeddings |
| Chatbot LLM | Ollama – Qwen 2.5 3B |
| Quality Evaluation | DeepEval |
| Quality Judge Model | Ollama – Qwen 2.5 7B |
| Security Judge Model | Ollama – Qwen 2.5 3B |
| Testing Framework | Pytest |
| Reports | JSON, Markdown |

**Model configuration:** Chatbot generation and LLM-based judging run locally through Ollama. Document embeddings use Google Gemini through its API.

---

## System Architecture

### 1. RAG Chatbot Pipeline

The Nivara Bank chatbot follows a Retrieval-Augmented Generation architecture.

1. **Document Ingestion:** Banking policy documents are loaded from the knowledge base.
2. **Text Splitting:** Documents are divided into smaller chunks using RecursiveCharacterTextSplitter.
3. **Embedding Generation:** Google Gemini Embeddings converts document chunks into vector representations.
4. **Vector Storage:** Chunks and their embeddings are stored in ChromaDB.
5. **Retrieval:** Relevant document chunks are retrieved based on the user's question.
6. **Response Generation:** Ollama's Qwen 2.5 3B generates an answer using the retrieved context.

### 2. Evaluation Pipeline

The evaluation framework consists of two main evaluation workflows.

**A. Functional and Quality Evaluation**

1. Load test cases from `golden_dataset.json`.
2. Execute questions against the Nivara Bank chatbot.
3. Capture generated answers and retrieval context.
4. Evaluate faithfulness and answer relevancy using DeepEval.
5. Compare metric scores against configured thresholds.
6. Identify cases that pass, fail, or require manual review.

**B. Security Evaluation**

1. Load security scenarios from `security_tests.json`.
2. Send test questions to the chatbot.
3. Capture chatbot responses and available policy context.
4. Evaluate responses against expected security behaviour using an LLM judge.
5. Record security verdicts and reasons.

**C. Report Generation**

The scoring module combines evaluation results and generates JSON and Markdown reports.

---

## Project Structure

```text
LLM-EvalSuite/
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── datasets/
│   ├── golden_dataset.json
│   └── security_tests.json
│
├── knowledge_base/
│   └── raw_documents/
│       ├── accounts_and_fees.txt
│       ├── cards_and_payments.txt
│       └── security_and_disputes.txt
│
├── src/
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── runner.py
│   │   ├── llm_judge.py
│   │   ├── json_utils.py
│   │   ├── quality_evaluator.py
│   │   ├── scoring.py
│   │   └── report_generator.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── ingest_documents.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── llm_client.py
│   │   └── prompt_template.py
│   │
│   └── retrieval/
│       └── retriever.py
│
├── tests/
│   ├── conftest.py
│   ├── test_advice_boundary.py
│   ├── test_answers.py
│   ├── test_judge_sanity.py
│   ├── test_quality.py
│   ├── test_retrieval.py
│   ├── test_runner.py
│   ├── test_security.py
│   └── test_unanswerable.py
│
├── scripts/
│   ├── check_chroma.py
│   ├── check_embeddings.py
│   └── check_gemini.py
│
├── reports/
│   ├── experiments.md
│   └── results_summary.md
│
├── experiment_deepeval.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── README.md
└── run_all.py
```

---

## Evaluation Metrics

The framework uses the following evaluation metrics:

| Metric | Description |
|---|---|
| Functional Pass Rate | Percentage of functional test cases classified as passed |
| Faithfulness | Measures whether generated answers are supported by retrieved context |
| Answer Relevancy | Measures how relevant generated answers are to user questions |
| Security Pass Rate | Percentage of security test cases classified as passed |

### Configured Thresholds

| Metric | Threshold |
|---|---:|
| Faithfulness | 0.70 |
| Answer Relevancy | 0.70 |

Cases with missing metric scores or predefined manual-review flags are not automatically counted as passes.

---

## Latest Evaluation Results

The following results were obtained from a successful execution of the complete evaluation pipeline.

| Evaluation Metric | Result |
|---|---:|
| Functional Pass Rate | 68% |
| Average Faithfulness | 0.90 |
| Average Answer Relevancy | 0.91 |
| Security Pass Rate | 100% |

**Result interpretation:** These results represent one evaluation run against the current datasets. Some functional cases require further investigation or manual review. A 100% security pass rate on this test dataset does not establish that the chatbot is completely secure.

### Generated Reports

After execution, the framework generates:

- `reports/quality_results.json` – Detailed functional, quality, and security evaluation results.
- `reports/results_summary.md` – Human-readable evaluation summary.

---

## Installation and Setup

### Prerequisites

- Python 3.12
- Git
- Ollama
- Google Gemini API key for document embeddings

### 1. Clone the Repository

```bash
git clone https://github.com/prachii31/LLM-EvalSuite.git

cd LLM-EvalSuite
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
LLM_MODEL=your_chat_model
EMBEDDING_MODEL=your_embedding_model
```

Use the model names configured by the project.

**Important:** The Gemini API key is used for document embeddings. Ollama handles local chatbot generation and LLM-based evaluation.

Never upload your actual `.env` file or API keys to GitHub.

### 5. Install Ollama Models

Install Ollama and pull the models used by the project:

```bash
ollama pull qwen2.5:3b

ollama pull qwen2.5:7b
```

Ensure the Ollama service is running before starting the chatbot or evaluation pipeline.

### 6. Build the Vector Database

Run the document ingestion module:

```bash
python -m src.ingestion.ingest_documents
```

This loads the banking policy documents, generates embeddings, and stores them in ChromaDB.

### 7. Run the Evaluation Framework

Execute the complete evaluation pipeline:

```bash
python run_all.py
```

The framework runs functional, quality, and security evaluations and generates reports in the `reports/` directory.

---

## Running Tests

Run the test suite using Pytest:

```bash
pytest -v
```

Run individual test modules:

```bash
pytest tests/test_retrieval.py -v

pytest tests/test_answers.py -v

pytest tests/test_security.py -v

pytest tests/test_unanswerable.py -v

pytest tests/test_advice_boundary.py -v

pytest tests/test_runner.py -v

pytest tests/test_judge_sanity.py -v
```

Quality evaluation tests use LLM-based judging and can take considerably longer than ordinary unit tests.

---

## Design Considerations

- The chatbot uses retrieved policy context to generate answers.
- Ollama provides local inference for chatbot generation and LLM-based judging.
- Gemini is used for document embeddings and requires an API key.
- DeepEval evaluates faithfulness and answer relevancy.
- Evaluation thresholds are configurable.
- Missing metric scores and selected cases requiring review are handled separately from automatic passes.
- Security test verdicts are based on the configured LLM judge and test scenarios.
- Nivara Bank is a fictional banking application intended for development and evaluation demonstrations, not real banking use.

---

## Future Improvements

- Expand functional and security test datasets.
- Improve consistency of LLM-based evaluation.
- Add more adversarial and edge-case test scenarios.
- Introduce regression tracking across evaluation runs.
- Explore additional evaluation metrics for RAG applications.

---

## Author

Developed as a hands-on project to explore:

**AI Quality Engineering | LLM Testing | RAG Evaluation | LLM Security Testing**

GitHub Repository: https://github.com/prachii31/LLM-EvalSuite