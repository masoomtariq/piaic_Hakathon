# ingest_docs.py
import os
import uuid
import sys
import asyncio
from google import genai
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from services.qdrant import generate_gemini_embedding
# Add the project root (one level above chatbot_backend) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from qdrant_client.models import VectorParams, Distance, PointStruct

# Load environment variables
# load_dotenv(dotenv_path=Path(__file__).parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("GEMINI_API_KEY not found in environment variables.")

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
if COLLECTION_NAME and QDRANT_HOST and QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
    )
else:
    print("QDRANT_API_KEY, QDRANT_HOST and COLLECTION_NAME not found in environment variables.")

# Create collection if it doesn't exist
if not client.collection_exists(COLLECTION_NAME):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )
else:
    print(f"Collection '{COLLECTION_NAME}' already exists.")

# Read and process documents
async def ingest_documents():
    docs_path = Path(__file__).parent / "book_source" / "docs"
    md_files = list(docs_path.rglob("*.md"))

    for doc_file in md_files:
        try:
            text = doc_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Failed to read {doc_file}: {e}")
            continue

        # Simple chunking by 500 characters
        chunks = [text[i:i+510] for i in range(0, len(text), 500)]
        points = []

        for chunk in chunks:
            embedding = await generate_gemini_embedding(chunk)
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),  # Safe UUID for Qdrant
                    vector=embedding,
                    payload={"text": chunk, "source": str(doc_file)}
                )
            )

        # Upsert points to Qdrant
        try:
            client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
        except Exception as e:
            print(f"Failed to upsert points for {doc_file}: {e}")

# Run ingestion
if __name__ == "__main__":
    asyncio.run(ingest_documents())
    print("Ingestion completed.")
