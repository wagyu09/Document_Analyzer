from konlpy.tag import Mecab
from rank_bm25 import BM25Okapi
class BM25Retriever:
    def __init__(self, dicpath):
        self.m = Mecab(dicpath = dicpath)
        self.bm25 = None
        self.corpus = None
    
    def add_documents(self, chunked_file):
        self.corpus = chunked_file
        seperated_chunks = []
        for chunk in chunked_file:
            seperated_chunks.append(self.m.morphs(chunk['chunk']))
        self.bm25 = BM25Okapi(seperated_chunks)
        
    
    def retrieve(self,  file_name, query, n = 7):
        seperated_query = self.m.morphs(query)
        top_n_docs = self.bm25.get_top_n(seperated_query, self.corpus, n = n)
        retrieved_data = ''
        for doc in top_n_docs:
            page = doc['page']
            chunk = doc['chunk']
            retrieved_data += f'source : {file_name}, page : {page}, \n content : {chunk} \n\n'
        
        return retrieved_data

