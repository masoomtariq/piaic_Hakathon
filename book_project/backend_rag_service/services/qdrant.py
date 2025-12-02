import os
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv

load_dotenv()

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

def generate_gemini_embedding(text: str):
    try:
        result = client.models.embed_content(
        model="text-embedding-004",
        contents=text)
        return result.embeddings
    except Exception as e:
        print(f"Error generating Gemini embedding: {e}")
        return []

def retrieve_context_from_qdrant(query_embedding, limit: int = 3, selected_text: str = None):
    search_params = {"hnsw_ef": 128, "exact": False}

    query_filter = None
    if selected_text:
        # If specific text is selected, try to prioritize documents containing that text
        # This is a simplified approach, a more advanced solution might involve re-ranking or keyword extraction
        query_filter = Filter(must=[
            FieldCondition(
                key="text",
                match=MatchValue(value=selected_text)
            )
        ])

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
        search_params=search_params,
    )

    context = []
    for hit in search_result:
        context.append({"text": hit.payload.get("text"), "source": hit.payload.get("source")})
    return context