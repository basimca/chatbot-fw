import chromadb
from chromadb.config import Settings
import google.generativeai as genai
import os
from typing import List, Dict, Any
import numpy as np

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))
        
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using Gemini
        """
        try:
            # Use Gemini's embedding model
            embedding = self.model.embed_content(text)
            return embedding.embedding
        except Exception as e:
            raise Exception(f"Error getting embedding: {str(e)}")
    
    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """
        Add a document to the vector store
        """
        try:
            # Generate embedding
            embedding = self.get_embedding(text)
            
            # Generate a unique ID
            doc_id = f"doc_{len(self.collection.get()['ids'])}"
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            
            return doc_id
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        """
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return formatted_results
        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
    
    def clear(self):
        """
        Clear all documents from the collection
        """
        try:
            self.collection.delete()
            self.collection = self.client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            raise Exception(f"Error clearing collection: {str(e)}") 