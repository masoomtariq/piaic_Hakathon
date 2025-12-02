import os
import uuid
import sys
from google import genai
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

# Import AFTER path fix and env load
load_dotenv()
from services.qdrant import generate_gemini_embedding # Verify this path matches your folder structure

# --- CONFIG ---
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not (COLLECTION_NAME and QDRANT_HOST and QDRANT_API_KEY):
    raise ValueError("Qdrant environment variables are missing.")

# Initialize Qdrant (Local instance for ingestion script)
qdrant_client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)

# Create collection if it doesn't exist
if not qdrant_client.collection_exists(COLLECTION_NAME):
    print(f"Creating collection: {COLLECTION_NAME}")
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
else:
    print(f"Collection '{COLLECTION_NAME}' already exists.")

def ingest_documents():
    
    docs_path = Path("/workspaces/Hakathon_project/book_project/book_source/docs")
    
    # Check if directory exists
    if not docs_path.exists():
        print(f"Error: Directory {docs_path} does not exist.")
        return

    md_files = list(docs_path.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files.")

    for doc_file in md_files:
        print(f"Processing: {doc_file.name}...")
        try:
            text = doc_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Failed to read {doc_file}: {e}")
            continue

        if not text:
            continue

        # Simple chunking
        chunk_size = 1350
        stride = 1200
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), stride)]
        
        points = []
        
        for i, chunk in enumerate(chunks):
            # FIX: Removed 'await' here
            embedding = generate_gemini_embedding(chunk)
            
            if not embedding:
                print(f"Skipping empty embedding for chunk {i}")
                continue

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk, 
                        "source": str(doc_file.name), # Store just filename or relative path usually
                        "full_path": str(doc_file)
                    }
                )
            )

        # Upsert points to Qdrant
        if points:
            try:
                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME, 
                    points=points, 
                    wait=True
                )
                print(f"Upserted {len(points)} chunks for {doc_file.name}")
            except Exception as e:
                print(f"Failed to upsert points for {doc_file}: {e}")

if __name__ == "__main__":
    ingest_documents()
    print("Ingestion completed.")