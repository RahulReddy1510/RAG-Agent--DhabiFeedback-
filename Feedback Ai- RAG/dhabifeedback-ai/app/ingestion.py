import os
import pickle
import numpy as np
import faiss
import pandas as pd
import PyPDF2
from sentence_transformers import SentenceTransformer
import sys

# Add parent dir to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from app.models import Document, SimpleTextSplitter

class DhabiIngester:
    def __init__(self):
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.splitter = SimpleTextSplitter(chunk_size=400, chunk_overlap=80)
        self.index_path = config.FAISS_INDEX_PATH
    
    def load_documents(self):
        docs = []
        
        # Load Feedback CSV
        csv_path = os.path.join(config.DATA_DIR, "feedback_sample.csv")
        if os.path.exists(csv_path):
            print(f"Loading feedback from {csv_path}...")
            try:
                df = pd.read_csv(csv_path)
                for index, row in df.iterrows():
                    # Combine all columns into content
                    content = f"Complaint: {row.get('complaint', '')}\nCategory: {row.get('category', '')}\nLocation: {row.get('location', '')}"
                    metadata = {"source": "feedback", "row": index}
                    docs.append(Document(content, metadata))
            except Exception as e:
                print(f"Error reading CSV: {e}")
        else:
            print("Warning: feedback_sample.csv not found.")

        # Load Policies PDFs
        policies_dir = config.POLICIES_DIR
        if os.path.exists(policies_dir):
            print(f"Loading policies from {policies_dir}...")
            for pdf in os.listdir(policies_dir):
                if pdf.endswith(".pdf"):
                    pdf_path = os.path.join(policies_dir, pdf)
                    print(f"  - {pdf}")
                    try:
                        reader = PyPDF2.PdfReader(pdf_path)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        docs.append(Document(text, {"source": pdf_path}))
                    except Exception as e:
                        print(f"Error reading PDF {pdf}: {e}")
        
        print(f"Total documents loaded: {len(docs)}")
        return docs
    
    def create_index(self):
        docs = self.load_documents()
        if not docs:
            print("No documents to index.")
            return

        print("Splitting documents...")
        chunks = self.splitter.split_documents(docs)
        print(f"Created {len(chunks)} chunks.")
        
        if not chunks:
            print("No chunks created.")
            return

        print("Encoding chunks...")
        embeddings = self.embedding_model.encode([c.page_content for c in chunks])
        
        # FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        os.makedirs(self.index_path, exist_ok=True)
        faiss.write_index(index, os.path.join(self.index_path, "index.faiss"))
        
        # Save chunks metadata
        with open(os.path.join(self.index_path, "chunks.pkl"), 'wb') as f:
            pickle.dump(chunks, f)
            
        print(f"Index saved to {self.index_path}")

if __name__ == "__main__":
    ingester = DhabiIngester()
    ingester.create_index()
