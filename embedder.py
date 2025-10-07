from sentence_transformers import SentenceTransformer
class Embedder:
    """Embeds chunked text to be stored in vector DB.
    
    This class turns the chunked text into the numerical vector which vector DB and retriever system can handle.
    """
    def __init__(self, model_name = 'intfloat/multilingual-e5-large-instruct'):
        """"Initializes the Embedder object
        
        Args: 
            model_name(str): The name of model which processes embedding.
            Defaults to 'intfloat/multilingual-e5-large-instruct' because it is known for decent performance in Korean. But, you can change it to another model if you want to.
        """
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, chunked_file : list):
        """Implements the embedding process.

        Args:
            chunked_file(list[dict]): The document data processed by Chunker.
        
        Returns:
            chunked_file(list[dict]): A list where each dictionary represents a page, chunked text and embedded text.
                        e.g., [{'page': 1, 'chunk' : '...', 'embedding' : [0.1,0.2...]}, ...]. 
            
        """
        chunk_text = [text['chunk'] for text in chunked_file]
        embedding = self.model.encode(chunk_text, convert_to_tensor=True)
        embedding = embedding.tolist()

        for idx, item in enumerate(chunked_file):
            item['embedding'] = embedding[idx]
        
        return chunked_file

