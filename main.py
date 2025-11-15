from pipeline.document_loader import DocumentLoader
from pipeline.chunker import Chunker
from pipeline.embedder import Embedder
from pipeline.vector_retriever import VectorRetriever
from pipeline.bm25_retriever import BM25Retriever
from pipeline.generator import Generator
import config
import os
from tkinter import filedialog

def setup_pipeline():
    chunker = Chunker(
        chunk_size = config.CHUNK_SIZE,
        overlap_size = config.OVERLAP_SIZE
    )
    print('Chunker loading completed')
    embedder = Embedder(
        model_name = config.EMBEDDING_MODEL
    )
    print('Embedder loading completed')
    vector_retriever =VectorRetriever(
        db_path = config.DB_PATH,
        model_name = config.EMBEDDING_MODEL,
        collection_name = config.COLLECTION_NAME
    )
    print('Vector Retriever loading completed')
    bm25_retriever = BM25Retriever(
        dicpath = config.DICPATH
    )
    print('BM25 Retriever loading completed')
    generator = Generator(
        model_name = config.LLM_NAME,
        options = config.DEFAULT_OLLAMA_OPTIONS
    )
    print('Generator loading completed')

    return chunker, embedder, vector_retriever, bm25_retriever, generator

def run_indexing(file_path, chunker, embedder, vector_retriever = None, bm25_retriever = None):
    loader = DocumentLoader(file_path = file_path)
    document = loader.load()
    chunks = chunker.chunking(document)
    embedded_chunks = embedder.embed_documents(chunks)
    file_name = os.path.basename(file_path)
    if vector_retriever != None:
        vector_retriever.add_documents(embedded_chunks, file_name)
    if bm25_retriever != None:
        bm25_retriever.add_documents(chunks, file_name)
    

if __name__ == "__main__":
    chunker, embedder, vector_retriever,bm25_retriever, generator = setup_pipeline()
    file_path = filedialog.askopenfilename()
    run_indexing(file_path, chunker, embedder, vector_retriever, None)
    query = input('Question : ')
    retrieved_data = bm25_retriever.retrieve(query,n_results = 5)
    outputs = generator.generate(retrieved_data,query)
    print(outputs)
    print(retrieved_data)



