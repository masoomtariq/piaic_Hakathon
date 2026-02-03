# piaic_hakathon

# Physical AI & Humanoid Robotics: The Interactive Textbook

## The Vision

**(Imagine this read aloud for an exciting product launch)**

Have you ever dreamed of building robots that can walk, see, and interact with the world? Of diving deep into Physical Artificial Intelligence, only to be stopped by a wall of complex mathematics, the steep learning curve of ROS 2, and the intimidating challenge of real-world hardware? You're not alone. For too long, this groundbreaking field has felt locked away, accessible only to a select few.

Until now.

Introducing the Physical AI & Humanoid Robotics Textbook – a project that redefines what a textbook can be. This is not a static book; it's a living, interactive guide, your personal mentor on an exciting journey into the future of robotics. We've torn down the barriers, transforming dense theory into intuitive, hands-on knowledge.

But we didn't stop there. What if you had a question at 2 AM? What if you needed a concept explained in a new way, right when you're feeling stuck?

Meet your personal, **24/7 Teaching Assistant**: the integrated AI Chatbot. Powered by Google's cutting-edge Gemini model, this isn't just a search bar. It's a conversational learning partner. Stuck on a line of code? Highlight it. Puzzled by a paragraph? Ask for a simpler explanation. The chatbot understands the context of what you're reading and provides instant, intelligent answers drawn directly from the course material. It’s like having an expert by your side, every step of the way.

This is more than a textbook. This is the future of education. A platform where curiosity is rewarded instantly, and the path to mastering robotics is clear, engaging, and truly inspiring. Welcome to the revolution.

## Technical Details

### Technology Stack

*   **Frontend:** A beautiful, responsive educational website built with **Docusaurus** and **React**.
*   **Backend:** A powerful and fast API service powered by **FastAPI**.
*   **AI & Search:**
    *   **Google Gemini LLM:** For state-of-the-art text generation and embeddings.
    *   **Qdrant Vector Database:** For lightning-fast, context-aware semantic search.
*   **Hosting:**
    *   Frontend deployed on **GitHub Pages**.
    *   Backend service hosted on **Render**.

### How It Works: Integration

The magic happens through a seamless integration between the frontend and backend. A custom **React Chatbot component** is embedded within the Docusaurus site. When you ask a question, this component sends a request to the **FastAPI backend hosted on Render**. The backend then uses the Qdrant vector database to find the most relevant sections of the textbook and feeds that context to the Gemini LLM to generate a precise, helpful answer, which is streamed back to you.

## Project Structure

```
Hakathon_project/
└───book_project/
    ├───CLAUDE.md
    ├───Hackathon I_ Physical AI & Humanoid Robotics Textbook.md
    ├───.specify/
    │   ├───memory/
    │   │   └───constitution.md
    │   └───templates/
    ├───agents/
    │   ├───__init__.py
    │   ├───base_agent.py
    │   └───subagent_chapter_summarizer/
    │       ├───__init__.py
    │       ├───agent.py
    │       └───test_agent.py
    ├───backend_rag_service/
    │   ├───__init__.py
    │   ├───conftest.py
    │   ├───ingest_docs.py
    │   ├───main.py
    │   ├───requirements.txt
    │   ├───services/
    │   │   ├───__init__.py
    │   │   ├───database.py
    │   │   ├───qdrant.py
    │   │   └───rag_service.py
    │   └───tests/
    │       ├───__init__.py
    │       ├───test_qdrant.py
    │       └───test_rag.py
    ├───book_source/
    │   ├───package-lock.json
    │   ├───package.json
    │   ├───sidebars.ts
    │   ├───tsconfig.json
    │   ├───blog/
    │   ├───docs/
    │   │   ├───assessments.md
    │   │   ├───hardware_requirements.md
    │   │   ├───introduction.md
    │   │   ├───module1_ros2.md
    │   │   ├───module2_digital_twin.md
    │   │   ├───module3_ai_robot_brain.md
    │   │   └───module4_vla.md
    │   ├───src/
    │   │   ├───components/
    │   │   │   ├───Chatbot.js
    │   │   │   ├───Chatbot.module.css
    │   │   │   └───HomepageFeatures/
    │   │   ├───css/
    │   │   ├───pages/
    │   │   │   ├───index.module.css
    │   │   │   ├───index.tsx
    │   │   │   └───markdown-page.md
    │   │   └───theme/
    │   │       └───Layout/
    │   └───static/
    ├───history/
    │   └───prompts/
    │       └───physical-ai-robotics-textbook/
    │           └───0001-run-project-debug-and-improve-ui-ux.misc.prompt.md
    └───specs/
        └───physical-ai-robotics-textbook/
            ├───plan.md
            ├───spec.md
            └───tasks.md
```

## Installation

To get this project running locally, you'll need to set up the frontend and backend separately.

### Frontend Setup (`book_source/`)

1.  **Navigate to the frontend directory:**
    ```bash
    cd book_source
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the local development server:**
    ```bash
    npm start
    ```
    The Docusaurus site will be available at `http://localhost:3000`.

### Backend Setup (`backend_rag_service/`)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend_rag_service
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    Create a `.env` file in this directory. You'll need to provide your credentials for the AI and vector database services.
    ```env
    GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
    QDRANT_HOST="your_qdrant_instance_host"
    QDRANT_API_KEY="your_qdrant_api_key_if_any"
    ```
5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The FastAPI service will be running at `http://localhost:8000`.
