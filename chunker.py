class Chunker:
    """Splits document text into manageable chunks using a sliding window strategy. 

    This class is a crucial process in the RAG pipeline. It prepares the chunked data from DocumentLoader for the subsequent embedding process.
    While I used a simple character-based chunking for this implementation, a word-based approach is necessary for improved RAG performance.
    """
    def __init__(self, chunk_size = 250 , overlap_size = 70 ):
        """Initializes the Chunker object

        Args: 
            chunk_size(int): The target maximum size of each chunk. Defaults to 250.
            overlap_size(int): The number of characters to overlap between consecutive chunks to maintain context. Defaults to 70
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def chunking(self, file : list):
        """Implements the chunking process.
        
        Args: 
            file(list[dict]): The document data processed by DocumentLoader.

        returns:
            chunked_text_list(list[dict]): A list where each dictionary represents a page, and chunked text.
                        e.g., [{'page': 1, 'chunk' : '...'}, ...]. 

        """
        chunked_text = []
        orphan_chunk = ''

        for page_data in file:
            page_number = page_data['page']
            content = page_data['content'] 

            for i in range(0,len(content), self.chunk_size-self.overlap_size):
                chunk =  content[i:i+self.chunk_size]

                if len(chunk) <= self.overlap_size:
                    orphan_chunk += chunk
                
                else:
                    chunk = orphan_chunk + chunk
                    chunked_text.append({'page' : page_number, 'chunk'  : chunk})
                    orphan_chunk = ''
                    
        if orphan_chunk != '':
            chunked_text.append({'page' : page_number, 'chunk'  : orphan_chunk})
        
        return chunked_text