# ingest_docs.py
import os
import asyncio
import logging
import uuid
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import sys
# Add the project root (one level above chatbot_backend) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from qdrant_client.models import VectorParams, Distance, PointStruct

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "book_content"

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Loaded QDRANT_HOST: {repr(QDRANT_HOST)}")
logger.debug(f"Loaded QDRANT_API_KEY: {repr(QDRANT_API_KEY)}")

if not QDRANT_HOST or not QDRANT_API_KEY:
    raise ValueError("QDRANT_HOST and QDRANT_API_KEY must be set in your .env file.")

# Connect to Qdrant
client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
logger.info(f"Connecting to Qdrant at: {QDRANT_HOST}")

# Create collection if it doesn't exist
if not client.collection_exists(COLLECTION_NAME):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE) # Gemini embedding-001 size
    )
    logger.info(f"Collection '{COLLECTION_NAME}' created.")
else:
    logger.info(f"Collection '{COLLECTION_NAME}' already exists.")

from chatbot_backend.app.services.qdrant import generate_gemini_embedding

# Read and process documents
async def ingest_documents():
    docs_path = Path(__file__).parent.parent / "website" / "docs"
    md_files = list(docs_path.rglob("*.md"))

    for doc_file in md_files:
        logger.info(f"Processing {doc_file}...")
        try:
            text = doc_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read {doc_file}: {e}")
            continue

        # Simple chunking by 500 characters
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
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
            logger.error(f"Failed to upsert points for {doc_file}: {e}")

# Run ingestion
if __name__ == "__main__":
    asyncio.run(ingest_documents())
    logger.info("Ingestion completed.")
