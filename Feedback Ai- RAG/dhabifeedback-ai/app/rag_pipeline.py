import os
import pickle
import faiss
import numpy as np
from ollama import Client
from sentence_transformers import SentenceTransformer
import sys

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from app.models import Document

class DhabiRAG:
    def __init__(self):
        # We reuse the same model as ingestion
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index_path = config.FAISS_INDEX_PATH
        self.ollama_client = Client(host=config.OLLAMA_BASE_URL)
        
    def retrieve(self, query, k=5):
        index_file = os.path.join(self.index_path, "index.faiss")
        chunks_file = os.path.join(self.index_path, "chunks.pkl")
        
        if not os.path.exists(index_file) or not os.path.exists(chunks_file):
            return []

        index = faiss.read_index(index_file)
        with open(chunks_file, 'rb') as f:
            chunks = pickle.load(f)
        
        query_emb = self.embedding_model.encode([query])
        distances, indices = index.search(np.array(query_emb).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(chunks):
                results.append((chunks[idx].page_content, chunks[idx].metadata, float(distances[0][i])))
        
        return results
    
    def generate_response(self, query, retrieved_docs):
        context = "\n\n".join([f"[{i+1}] {doc[0]}" for i, doc in enumerate(retrieved_docs)])
        
        prompt = f"""
        You are a smart city assistant for the Dubai/Abu Dhabi government. 
        Your goal is to analyze citizen feedback and provide a structured, actionable response based on government policies.

        CITIZEN FEEDBACK: {query}

        RELEVANT POLICIES/CONTEXT:
        {context}

        INSTRUCTIONS:
        Respond in a professional "Government Officer" tone.
        If the query is in Arabic, respond in Arabic. If English, respond in English.
        
        Structure your response exactly as follows:
        **PRIORITY**: [High/Medium/Low]
        **AGENCY**: [Relevant Entity, e.g., RTA, DEWA, Dubai Municipality]
        **ACTION PLAN**:
        1. [Step 1]
        2. [Step 2]
        **RELEVANT POLICY**: [Cite specific rules from context if available]
        """
        
        try:
            stream = self.ollama_client.generate(model=config.OLLAMA_MODEL, prompt=prompt, stream=True)
            for chunk in stream:
                yield chunk['response']
        except Exception as e:
            yield f"Error connecting to Ollama: {str(e)}. Please ensure Ollama is running (`ollama serve`)."

if __name__ == "__main__":
    rag = DhabiRAG()
    # Test
    q = "Heavy traffic on Sheikh Zayed Road"
    docs = rag.retrieve(q)
    print(rag.generate_response(q, docs))
