import pymupdf
import re

class DocumentLoader:
    """Loads and preprocesses text from a PDF document.

    This class is the first step in the RAG pipeline. It handles opening
    a PDF file, extracting raw text from each page, and performing
    initial cleaning. The output is a structured list ready for the 
    Chunker module.
    """
    def __init__(self, file_path : str):
        """Initializes the DocumentLoader object.

        Args: 
            file_path(str): The path to the pdf file to be processed
        """
        self.file_path = file_path
    
    @staticmethod
    def clean_text(text : str):
        """ Removes unnecessary whitespace and strings.
        Args: 
            text(str): The input text to clean

        Returns:
            str: The cleaned text.
        """
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\.+','', text)
        text = re.sub(r'전자공시시스템\s*dartfssorkr\s*Page\s*\d+','',text)

        return text.strip()
    
    def load(self):
        """ Loads the PDF file, extracts text from each page, and returns a list of dictionaries.

        Returns:
            full_text(list[dict]): A list where each dictionary represents a page,
                        e.g., [{'page': 1, 'content': '...'}, ...]."""
        doc = pymupdf.open(self.file_path)
        full_text = []
        for page ,content in enumerate(doc,start=1):
            text = content.get_text()
            cleaned_text = DocumentLoader.clean_text(text)
            full_text.append({'page' : page, 'content' : cleaned_text})
        
        return full_text
