from konlpy.tag import Mecab
from rank_bm25 import BM25Okapi
class BM25Retriever:
    def __init__(self, dicpath):
        self.m = Mecab(dicpath = dicpath)
        self.bm25 = None
        self.corpus = None
        self.file_name = None
    
    def add_documents(self, chunked_file, file_name):
        self.corpus = chunked_file
        self.file_name = file_name
        separated_chunks = []
        for chunk in chunked_file:
            separated_chunks.append(self.m.morphs(chunk['chunk']))
        self.bm25 = BM25Okapi(separated_chunks)
        
    
    def retrieve(self, query, n_results = 5):
        separated_query = self.m.morphs(query)
        top_n_docs = self.bm25.get_top_n(separated_query, self.corpus, n = n_results)
        retrieved_data = ''
        for doc in top_n_docs:
            page = doc['page']
            chunk = doc['chunk']
            retrieved_data += f'source : {self.file_name}, page : {page}, \n content : {chunk} \n\n'
        
        return retrieved_data

