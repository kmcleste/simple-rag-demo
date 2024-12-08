import os
from pathlib import Path

import chromadb


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(Path(os.getcwd(), "data")))
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, texts, metadatas, ids):
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)

    def query(self, query_text, n_results=3, **kwargs):
        return self.collection.query(
            query_texts=[query_text], n_results=n_results, **kwargs
        )
