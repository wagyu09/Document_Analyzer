# Chunker settings
CHUNK_SIZE = 250
OVERLAP_SIZE = 70

# Retriever & Embedder settings
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
DB_PATH = "chroma_db"
COLLECTION_NAME = "documents_collection"
DICPATH = "/home/wagyu0923/miniconda3/envs/exaone/lib/mecab/dic/mecab-ko-dic"

# Generator settings
LLM_NAME = 'gemma2:9b'
DEFAULT_OLLAMA_OPTIONS = {
    'temperature': 0.0,
    'repeat_penalty': 1.1,
    'seed': 42,
    'num_predict' : 4096
}
