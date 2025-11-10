import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    
    def __init__(self, file_path=None, uploaded_file=None, data=None):
        """
        Initialize Portfolio with either a DataFrame, uploaded file, or default file path.
        """
        if data is not None:
            self.data = data
            self.file_source = "Provided DataFrame"
        elif uploaded_file is not None:
            self.data = pd.read_csv(uploaded_file)
            self.file_source = f"Uploaded: {uploaded_file.name}"
        elif file_path is not None and os.path.exists(file_path):
            self.data = pd.read_csv(file_path)
            self.file_source = f"Default: {file_path}"
        else:
            raise FileNotFoundError(
                f"No valid portfolio file found. Please upload a CSV or ensure default file exists at: {file_path}"
            )
        
        self.chroma_client = chromadb.PersistentClient("vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name='portfolio')
    
    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row['Techstack'],
                    metadatas={"links": row['Links']},
                    ids=[str(uuid.uuid4())]
                )
    
    def get_quiery(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
