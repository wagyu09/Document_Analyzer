import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import numpy as np

class VectorRetriever:
    """
    Manages storing and retrieving data from a ChromaDB vector store
    
    This class connects to the vector database, adds processed documents with their metadata, and finds the most relevant chunks for a given query
    """
    def __init__(self, db_path = 'chroma_db', model_name = "intfloat/multilingual-e5-large-instruct", collection_name = 'documents_collection'):
        """Initializes the VectorRetriever object
        
        Args:
            db_path(str): The path that persistent database is stored.
            model_name(str): The name of the SentenceTransformer model that the collection will use as its embedding function.
            collection_name(str): The name of the collection to use within the database.
        """
        self.embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name = model_name)
        self.client = chromadb.PersistentClient(path = db_path)
        self.collection = self.client.get_or_create_collection(
            name = collection_name,
            embedding_function = self.embedding_model
        )


    def add_documents(self, embedded_file : list, file_name : str):
        ids = []
        meta_datas = []
        embeddings = []
        chunks = []

        for idx, data in enumerate(embedded_file):
            meta_data = {}
            meta_data['source'] = file_name
            meta_data['page'] = data['page']
            meta_datas.append(meta_data)

            chunks.append(data['chunk'])
            embeddings.append(data['embedding'])
            ids.append(f'{file_name}_chunk_{idx}')

        self.collection.add(
        embeddings = embeddings,
        metadatas = meta_datas,
        ids = ids,
        documents=chunks
        )
        
    def retrieve(self, query : str, n_results = 7):
        collected_data = self.collection.query(
            query_texts = [query],
            n_results = n_results
        )
        retrived_data = ''

        for meta, chunk in zip(collected_data['metadatas'][0], collected_data['documents'][0]):
            source = meta['source']
            page = meta['page']
            retrived_data += f'source : {source}, page : {page}, \n content : {chunk} \n\n'
        
        return query, retrived_data