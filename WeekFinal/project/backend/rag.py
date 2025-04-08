import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGSystem:
    def __init__(self):
        # Initialize the embedding model
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Initialize ChromaDB
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="japanese-learning",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents, metadatas=None, ids=None):
        """Add documents to the collection"""
        # Generate embeddings
        embeddings = self.model.encode(documents)
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=[emb.tolist() for emb in embeddings],
            metadatas=metadatas if metadatas else [{}] * len(documents),
            ids=ids if ids else [f"doc_{i}" for i in range(len(documents))]
        )

    def query(self, query_text, n_results=2):
        """Query the collection"""
        # Generate query embedding
        query_embedding = self.model.encode(query_text)
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        return results

if __name__ == "__main__":
    # Example usage
    rag = RAGSystem()
    
    # Add some example documents
    documents = [
        "This is document1", 
        "This is document2"
    ]
    rag.add_documents(documents)
    
    # Query example
    results = rag.query("This is a query document")
    print(results)