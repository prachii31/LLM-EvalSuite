# LLM-EvalSuite
### A Lightweight Framework for Evaluating RAG Chatbot Quality and Security

LLM-EvalSuite is a Python-based evaluation framework designed to assess the quality, reliability, and security of Large Language Model (LLM) applications.

The project uses a fictional banking chatbot, **Nivara Bank**, as the application under test. It evaluates chatbot responses against a golden dataset, measures response quality using DeepEval, and checks security-related behaviour using LLM-based judging.

The framework generates structured JSON and Markdown reports to make evaluation results easier to inspect and understand.

## Key Features

- **Functional Testing:** Tests chatbot responses against predefined questions and expected behaviour.
- **Faithfulness Evaluation:** Uses DeepEval to assess whether answers are supported by retrieved context.
- **Answer Relevancy Evaluation:** Measures how relevant generated answers are to user questions.
- **Security Testing:** Evaluates behaviour against prompt injection, credential disclosure, privacy violations, and unsafe banking claims.
- **Automated Scoring:** Calculates functional and security pass rates along with average quality scores.
- **Report Generation:** Generates JSON and Markdown evaluation reports.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Google Gemini Embeddings |
| Chatbot LLM | Ollama – Qwen 2.5 3B |
| Quality Evaluation | DeepEval |
| Quality Judge Model | Ollama – Qwen 2.5 7B |
| Security Judge Model | Ollama – Qwen 2.5 3B |
| Testing Framework | Pytest |
| Reports | JSON, Markdown |

## System Architecture

### 1. Chatbot Pipeline

1. Banking documents are loaded from the knowledge base.
2. Documents are split into smaller chunks.
3. Gemini embeddings convert the chunks into vector representations.
4. Chunks are stored in ChromaDB.
5. A user question is used to retrieve relevant context.
6. Qwen 2.5 3B generates an answer using the retrieved context.

### 2. Evaluation Pipeline

**Functional and quality evaluation:**

1. Load test cases from the golden dataset.
2. Execute each question against the Nivara Bank chatbot.
3. Capture the generated answer and retrieval context.
4. Evaluate faithfulness and answer relevancy using DeepEval.
5. Calculate scores using configured thresholds.
6. Generate JSON and Markdown reports.

**Security evaluation:**

1. Load security test cases.
2. Send each test question to the chatbot.
3. Capture its response.
4. Evaluate the response against the expected security behaviour.
5. Record PASS, FAIL, or ERROR verdicts and generate the report.

## Project Structure

```text
AI-Chatbot-Quality-Evaluation/
│
├── config/
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
│   │   ├── runner.py
│   │   ├── llm_judge.py
│   │   ├── json_utils.py
│   │   ├── quality_evaluator.py
│   │   ├── scoring.py
│   │   └── report_generator.py
│   │
│   ├── ingestion/
│   │   └── ingest_documents.py
│   │
│   ├── rag/
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
├── reports/
│   ├── quality_results.json
│   ├── results_summary.md
│   └── experiments.md
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
└── run_all.py
```

## Evaluation Metrics

The framework uses the following metrics:

| Metric | Purpose |
|---|---|
| Functional Pass Rate | Measures the percentage of functional test cases that pass |
| Faithfulness | Checks whether answers are supported by retrieved context |
| Answer Relevancy | Checks whether answers address the user's question |
| Security Pass Rate | Measures the percentage of security test cases that pass |

The configured quality thresholds are:

- Faithfulness: 0.70
- Answer Relevancy: 0.70

Cases requiring manual review are identified separately rather than being treated as automatic passes.

## Latest Evaluation Results

The following results were obtained from a successful execution of `python run_all.py`.

| Metric | Result |
|---|---:|
| Functional Pass Rate | 68% |
| Average Faithfulness | 0.90 |
| Average Answer Relevancy | 0.91 |
| Security Pass Rate | 100% |

**Note:** These are results from the current evaluation run and test datasets. A 100% security pass rate does not establish that the chatbot is completely secure. Quality scores and flagged cases should also be reviewed before drawing conclusions.

## Installation and Setup

### Prerequisites

- Python 3.12
- Git
- Ollama
- Google Gemini API key for embeddings

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Chatbot-Quality-Evaluation
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add your Gemini API key and the required model configuration.

```env
GEMINI_API_KEY=your_gemini_api_key
LLM_MODEL=your_chat_model
EMBEDDING_MODEL=your_embedding_model
```

Do not commit your actual `.env` file or API keys to GitHub.

### 5. Install the Ollama models

```bash
ollama pull qwen2.5:3b
ollama pull qwen2.5:7b
```

Make sure Ollama is running before executing the chatbot and evaluation pipeline.

### 6. Build the vector database

```bash
python -m src.ingestion.ingest_documents
```

### 7. Run the evaluation framework

```bash
python run_all.py
```

## Running Tests

Run the Pytest suite:

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
```

## Generated Reports

After running the evaluation pipeline, reports are generated in the `reports/` directory:

- `quality_results.json` – Detailed functional, quality, and security evaluation results.
- `results_summary.md` – Human-readable evaluation summary.
- `experiments.md` – Experiment notes and observations.

## Design Considerations

- Local Ollama models are used for chatbot generation and LLM-based judging.
- Gemini embeddings require an API key and are subject to the provider's usage limits.
- Evaluation thresholds are configurable.
- Cases with missing or unreliable metric scores are not automatically counted as passes.
- The banking application uses fictional policy information and is intended for testing and demonstration, not real banking use.

## Future Improvements

- Expand the golden and security test datasets.
- Improve consistency of LLM-based evaluation.
- Add more adversarial and edge-case test scenarios.
- Introduce regression tracking across evaluation runs.

## Author

Developed as a hands-on project to explore **AI Quality Engineering, LLM Testing, RAG Evaluation, and LLM Security Testing**.