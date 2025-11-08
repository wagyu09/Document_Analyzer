# Chunker settings
CHUNK_SIZE = 250
OVERLAP_SIZE = 70

# Retriever & Embedder settings
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
DB_PATH = "chroma_db"
COLLECTION_NAME = "documents_collection"


# Generator settings
LLM_NAME = 'gpt-oss:20b'
DEFAULT_OLLAMA_OPTIONS = {
    'temperature': 0.1,
    'repeat_penalty': 1.1,
    'seed': 42
}
