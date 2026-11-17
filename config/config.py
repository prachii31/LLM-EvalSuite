
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Document processing configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval configuration
TOP_K = 3

# Evaluation thresholds
FAITHFULNESS_THRESHOLD = 0.7
ANSWER_RELEVANCY_THRESHOLD = 0.7

# Project paths
KNOWLEDGE_BASE_PATH = (
    PROJECT_ROOT / "knowledge_base" / "raw_documents"
)

CHROMA_PATH = PROJECT_ROOT / "storage" / "chroma_db"

CACHE_PATH = PROJECT_ROOT / "cache"
REPORTS_PATH = PROJECT_ROOT / "reports"
DATASETS_PATH = PROJECT_ROOT / "datasets"


def validate_config():
    """Validate required Gemini configuration."""

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    if not LLM_MODEL:
        raise ValueError("LLM_MODEL is missing from .env")

    if not EMBEDDING_MODEL:
        raise ValueError("EMBEDDING_MODEL is missing from .env")

    print("Configuration loaded successfully!")


if __name__ == "__main__":
    validate_config()
