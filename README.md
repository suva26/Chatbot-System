# Chatbot System (FastAPI, Modular, AI-ready)

A modular Python backend for ChatGPT-like chat, document AI, and AI-enabled APIs.

## What is improved (ChatGPT-like behavior)

- Multi-turn sessions with conversation memory persisted in SQLite.
- System prompt + temperature controls per request.
- Real OpenAI Chat Completions + Embeddings path when `openai_api_key` is provided in `.env`.
- Safe fallback stub behavior when credentials or SDK are missing.
- RAG-style context injection from ingested documents.

## Architecture

- `app/api`: FastAPI routes
- `app/services`: Business logic (`chat`, `document`, `data`, `ml_exposure`)
- `app/integrations/providers`: LLM + embedding adapters
- `app/integrations/vectorstores`: in-memory vector search + cloud extension points
- `app/agents`: LangGraph/CrewAI availability exposure

## API Endpoints

- `GET /` → ChatGPT-style web UI.

- `POST /api/chat` → Chat with memory (`session_id`) and model controls.
- `POST /api/documents/ingest` → Chunk + embed + store.
- `POST /api/documents/retrieve` → Similarity search.
- `GET /api/system/runtime` → Runtime capability status.
- `GET /api/analytics/conversations` → SQL/pandas/numpy stats.


## Web Frontend

- Open `/` for a ChatGPT-like UI (sidebar settings + chat window + composer).
- The frontend calls `POST /api/chat` and preserves `session_id` for multi-turn memory.
- Static frontend assets live in `frontend/` and are served by FastAPI at `/frontend/*`.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`

## Example chat request

```json
{
  "user_id": "user-1",
  "session_id": null,
  "message": "Explain vector databases in simple terms",
  "system_prompt": "You are a helpful AI assistant.",
  "temperature": 0.3
}
```

## Docker

```bash
docker compose up --build
```

## Production notes

- Replace generic provider stubs for Groq/Gemini/Claude with official SDK calls.
- Implement `PgVectorStore`/`PineconeStore` methods for production vector retrieval.
- Add auth/rate-limits and observability before public deployment.
