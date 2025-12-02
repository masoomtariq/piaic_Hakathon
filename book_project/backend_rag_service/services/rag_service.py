import os
from google import genai
from google.genai import types
from .qdrant import retrieve_context_from_qdrant, generate_gemini_embedding

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("GEMINI_API_KEY not found in environment variables.")

def generate_rag_response(user_query: str, selected_text: str = None) -> str:

    # 1. Generate embedding for the user query
    query_embedding = generate_gemini_embedding(user_query)
    if not query_embedding:
        return "Error: Could not generate embedding for the query."

    # 2. Retrieve relevant context from Qdrant
    context = retrieve_context_from_qdrant(query_embedding, selected_text=selected_text)

    if not context:
        return "I couldn't find any relevant information in the textbook to answer your question."

    # 3. Construct prompt for Gemini with retrieved context
    context_str = "\n".join([doc["text"] for doc in context])
    prompt = f"You are a helpful assistant for a Physical AI & Humanoid Robotics textbook. Answer the user's question based ONLY on the following context. If the answer is not in the context, state that you don't know.\n\nContext:\n{context_str}"
    if selected_text:
        prompt = prompt + f"\n\n Plus Point: \n\tFrom the context, the user has also highlighted this text: {selected_text}"

    # 4. Generate response using Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=prompt),
                contents=user_query
                )
        return response.text
    except Exception as e:
        print(f"Error generating Gemini response: {e}")
        return "An error occurred while generating the response."
