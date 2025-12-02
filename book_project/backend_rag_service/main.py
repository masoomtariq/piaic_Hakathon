import os
from google import genai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, Body
from typing import Annotated
from services.rag_service import generate_rag_response

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    client = genai.Client(GEMINI_API_KEY)
else:
    print("GEMINI_API_KEY not found in environment variables. Please set it.")

app = FastAPI()

# Configure CORS
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),  # Frontend URL for Docusaurus development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Textbook Chatbot Backend!"}

@app.post("/rag/chat", tags=["rag"])
async def chat_endpoint(
    user_query: Annotated[str, Body(..., description="The user's query")],
    selected_text: Annotated[str | None, Body(description="Optional selected text from the document for context")] = None
):
    """
    Handles RAG chat queries.
    """
    try:
        response = await generate_rag_response(user_query, selected_text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))