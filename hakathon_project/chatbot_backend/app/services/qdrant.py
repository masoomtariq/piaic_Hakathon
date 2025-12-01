import os
import google.generativeai as genai
from qdrant_client import QdrantClient, models

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Removed redundant API key retrieval

# genai.configure(api_key=GEMINI_API_KEY) # Removed redundant API configuration

qdrant_client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)

def get_qdrant_client() -> QdrantClient:
    return qdrant_client

def generate_gemini_embedding(text: str) -> list[float]:
    try:
        response = genai.embed_content(model="models/embedding-001", content=text)
        return response['embedding']
    except Exception as e:
        print(f"Error generating Gemini embedding: {e}")
        return []
