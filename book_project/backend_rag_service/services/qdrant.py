import os
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv

load_dotenv()

# --- GEMINI SETUP ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("GEMINI_API_KEY not found.")
    client = None # Handle missing client safely

# --- QDRANT SETUP ---
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if COLLECTION_NAME and QDRANT_HOST and QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
    )
else:
    print("QDRANT keys missing.")
    qdrant_client = None

def generate_gemini_embedding(text: str):
    """
    Generates an embedding vector for the given text.
    """
    if not client:
        return []
    try:
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        if result.embeddings:
            return result.embeddings[0].values
        return []
    except Exception as e:
        print(f"Error generating Gemini embedding: {e}")
        return []

def retrieve_context_from_qdrant(query_embedding, limit: int = 3, selected_text: str = None):
    """
    Retrieves context. 
    """
    if not qdrant_client:
        return []

    search_params = {"hnsw_ef": 128, "exact": False}

    query_filter = None
    
    if selected_text:
        query_filter = Filter(must=[
            FieldCondition(
                key="source", 
                match=MatchValue(value=selected_text)
            )
        ])

    try:
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
            context.append({
                "text": hit.payload.get("text"), 
                "source": hit.payload.get("source"),
                "score": hit.score # Good to see match score
            })
        return context
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return []