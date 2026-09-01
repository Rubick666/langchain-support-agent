# Support Agent (langchain-support-agent)

A conversational customer-support agent built with LangChain, FastAPI, Redis, ChromaDB, and Ollama.

## Quick Start

1. Clone the repo.
2. Run `docker-compose up --build`.
3. Visit `http://localhost:8000/health` to verify services.
4. API docs at `http://localhost:8000/docs`.

## Chat Endpoint

`POST /chat/` – streams a response using SSE.

**Request:**

```json
{
  "session_id": "test-session",
  "message": "How often should I change my oil?"
}
```
