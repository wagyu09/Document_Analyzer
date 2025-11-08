from pipeline.document_loader import DocumentLoader
from pipeline.chunker import Chunker
from pipeline.embedder import Embedder
from pipeline.vector_retriever import VectorRetriever
from pipeline.generator import Generator
import config
import os
from tkinter import filedialog

def setup_pipeline():
    chunker = Chunker(
        chunk_size = config.CHUNK_SIZE,
        overlap_size = config.OVERLAP_SIZE
    )
    print('Chunking Complete')
    embedder = Embedder(
        model_name = config.EMBEDDING_MODEL
    )
    print('Embedding Complete')
    retriever =VectorRetriever(
        db_path = config.DB_PATH,
        model_name = config.EMBEDDING_MODEL,
        collection_name = config.COLLECTION_NAME
    )
    print('Retrieving Coplete')
    generator = Generator(
        model_name = config.LLM_NAME,
        options = config.DEFAULT_OLLAMA_OPTIONS
    )
    return chunker, embedder, retriever, generator

def run_indexing(file_path, chunker, embedder, retriever):
    loader = DocumentLoader(file_path = file_path)
    document = loader.load()
    chunks = chunker.chunking(document)
    embedded_chunks = embedder.embed_documents(chunks)
    file_name = os.path.basename(file_path)
    retriever.add_documents(embedded_chunks, file_name)

if __name__ == "__main__":
    chunker, embedder, retriever, generator = setup_pipeline()
    file_path = filedialog.askopenfilename()
    run_indexing(file_path, chunker, embedder, retriever)
    query = input('Question : ')
    retrieved_data = retriever.retrieve(query,n_results = 5)
    outputs = generator.generate(retrieved_data,query)
    print(outputs)
    print(retrieved_data)



