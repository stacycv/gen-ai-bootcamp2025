from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
import boto3

class QuestionVectorStore:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.embeddings = BedrockEmbeddings(
            client=self.bedrock_client,
            model_id="amazon.titan-embed-text-v1"  # or your preferred embedding model
        )
        self.vector_store = None

    def create_vector_store(self, questions):
        """Create vector store from list of questions"""
        texts = [q["text"] for q in questions]
        metadata = [{"section": q["section"], "type": q["type"]} for q in questions]
        
        self.vector_store = FAISS.from_texts(
            texts,
            self.embeddings,
            metadatas=metadata
        )
        
    def find_similar_questions(self, query: str, k: int = 3):
        """Find k most similar questions to the query"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        return self.vector_store.similarity_search(query, k=k) 