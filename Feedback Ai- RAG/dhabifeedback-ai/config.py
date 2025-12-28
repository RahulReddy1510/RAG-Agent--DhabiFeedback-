import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
POLICIES_DIR = os.path.join(DATA_DIR, 'policies')
VECTORSTORE_DIR = os.path.join(BASE_DIR, 'vectorstore')
FAISS_INDEX_PATH = os.path.join(VECTORSTORE_DIR, 'faiss_index')

# Ollama Settings
OLLAMA_MODEL = "llama3:latest"
OLLAMA_BASE_URL = "http://localhost:11434"
