"""Application configuration."""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAISS_INDEX_PATH = DATA_DIR / "faiss_index" / "medical_index.faiss"
FAISS_METADATA_PATH = DATA_DIR / "faiss_index" / "metadata.json"
DOCUMENTS_DIR = DATA_DIR / "documents"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "faiss_index").mkdir(exist_ok=True)
DOCUMENTS_DIR.mkdir(exist_ok=True)

# API Configuration
API_KEY = os.getenv("API_KEY", "T1-ai-secret-key-2025")
API_TITLE = "Healthcare RAG Assistant"
API_VERSION = "1.0.0"

# FAISS Configuration
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
FAISS_DIMENSION = 384  # Dimension of MiniLM model
CHUNK_SIZE = 512
TOP_K_RESULTS = 3

# Language Configuration
SUPPORTED_LANGUAGES = ["en", "ja"]
DEFAULT_LANGUAGE = "en"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
