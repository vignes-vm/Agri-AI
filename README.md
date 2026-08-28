# Agri-AI

Agri-AI is a Flask-based backend API that provides an agriculture assistant chatbot powered by Google Gemini, along with crop information and sample order-tracking endpoints.

It is designed for easy integration with mobile or web clients and includes:
- Conversational farming guidance
- Intent-aware responses (crop info, pest/disease, fertilizers, yield, order tracking)
- Local agriculture dataset support (crops + orders)
- REST endpoints for chat, search, statistics, and utility features

## Tech Stack

- Python 3.x
- Flask + Flask-CORS
- Google Generative AI (Gemini)
- python-dotenv for environment configuration

## Features

- Chat endpoint with per-user conversation history
- Lightweight intent detection to improve response relevance
- Knowledge-base augmentation for common agriculture topics
- Data-driven context injection from local JSON files:
	- Crop details (season, soil, climate, cultivation, pests, diseases)
	- Order details (status tracking by order ID and user)
- Health check and API statistics endpoints
- CORS enabled for client integration

## Project Structure

```text
Agri-AI/
├── app.py                      # Flask app factory and server startup
├── config.py                   # Environment + model configuration
├── check_models.py             # Utility script to list available Gemini models
├── requirements.txt            # Python dependencies
├── data/
│   ├── crops.json              # Crop dataset
│   ├── orders.json             # Orders dataset
│   └── products.csv            # Product reference data
├── models/
│   └── agriculture_data.py     # Data loading/search/format helpers
├── routes/
│   └── chat_routes.py          # REST API endpoints
└── services/
    ├── chatbot_service.py      # Chat orchestration + Gemini integration
    └── knowledge_base.py       # Built-in agriculture knowledge snippets
```

## API Overview

Base URL (local): `http://localhost:5000`

Root endpoint:
- `GET /` - API metadata and endpoint summary

Chat and session endpoints:
- `POST /api/chat`
- `POST /api/clear-history`
- `GET /api/conversation-history/<user_id>`

Crop endpoints:
- `GET /api/crops`
- `GET /api/crop/<crop_name>`
- `GET /api/search-crops?q=<query>`

Order endpoints:
- `GET /api/order/<order_id>`
- `GET /api/user-orders/<user_id>`

Utility endpoints:
- `GET /api/health`
- `GET /api/quick-questions`
- `GET /api/statistics`

## Setup and Run

### 1. Clone and move into the project

```bash
git clone <your-repo-url>
cd Agri-AI
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_ai_api_key
SECRET_KEY=replace_with_secure_value
FLASK_DEBUG=True
PORT=5000
```

Notes:
- `GOOGLE_API_KEY` is required for chatbot responses.
- `OPENAI_API_KEY` appears in configuration but is not required by the current Gemini-based runtime flow.

### 5. Start the server

```bash
python app.py
```

Server will start on:
- `http://localhost:5000`

Health check:
- `http://localhost:5000/api/health`

## Request/Response Examples

### Chat

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER123",
    "message": "How to grow rice?"
  }'
```

Sample response:

```json
{
  "success": true,
  "response": "...",
  "intent": "crop_info"
}
```

### Track an Order

```bash
curl http://localhost:5000/api/order/ORD001
```

### Search Crops

```bash
curl "http://localhost:5000/api/search-crops?q=kharif"
```

## Data Included

Bundled sample datasets include:
- `5` crops in `data/crops.json`
- `3` orders in `data/orders.json`
- Product reference rows in `data/products.csv`

These can be expanded to fit your local market and crop conditions.

## Configuration Notes

Main configuration lives in `config.py`:
- Model name: `models/gemini-pro-latest`
- Temperature: `0.7`
- Max tokens: `500`
- API server port from `PORT` environment variable

You can verify available Gemini models with:

```bash
python check_models.py
```

## Error Handling

The API returns JSON error objects with `success: false` and an `error` message for:
- Missing or empty request input
- Resource not found (e.g., unknown crop/order)
- Internal runtime exceptions

Global handlers exist for:
- `404` endpoint not found
- `500` internal server error

## Limitations and Future Improvements

- Conversation history is in-memory (not persistent).
- No authentication/authorization layer yet.
- No test suite currently included.
- `products.csv` is not currently used directly by API logic.

Recommended next steps:
- Add persistent storage (SQLite/PostgreSQL/Redis)
- Add automated tests (unit + API integration)
- Add auth and rate limiting for production
- Add logging and observability

## SPSIL Analysis

### Situation

Farmers and agri-app users need fast, reliable answers to everyday farming questions (crop cultivation, pests, fertilizers, irrigation, yield) as well as visibility into their own orders (seeds, fertilizer, equipment), typically from a mobile app. Sending every query straight to a general-purpose LLM is slow to integrate, hard to make consistent, and has no access to the app's own data (crop database, order status). Agri-AI was built as the backend service to fill that gap: a Flask REST API that a mobile or web client can call for both conversational guidance and structured data (crops, orders, statistics).

### Problem

- **No unified, app-aware chat backend.** Farmers asking "How to grow rice?" or "Where is my order ORD001?" need one endpoint that understands both agriculture and the app's own order/crop records — a plain LLM call can't see `data/orders.json` or `data/crops.json` on its own.
- **Generic LLM answers lack grounding.** Without injecting structured local data (crop season, soil type, cultivation steps) and curated knowledge-base snippets (organic farming, IPM, irrigation methods), Gemini's raw answers would be generic and not tied to the app's own dataset.
- **Session/state handling for a stateless mobile client.** The mobile app needs per-user conversation continuity (`user_id`) without managing chat state itself.
- **Latent implementation issues found while reviewing the code:**
  - `app.py:21` prints `"Please set OPENAI_API_KEY in .env file"` on a config validation failure, but `Config.validate()` (`config.py:30`) actually checks `GOOGLE_API_KEY` — a misleading error message that would send a developer chasing the wrong variable.
  - `requirements.txt` pulls in `openai`, `langchain`, `langchain-openai`, `chromadb`, and `sentence-transformers`, none of which are imported anywhere in the runtime code (only `google-generativeai`, `flask`, `flask-cors`, and `python-dotenv` are actually used) — unnecessary install weight and confusion about which LLM provider is active.
  - `config.py:17-18` has a comment (`# --- FIX: Change the model name ---`) documenting that an earlier model name (`gemini-1.5-flash`) had to be swapped out, evidence that model availability/deprecation was already hit once.
  - Conversation history (`ChatbotService.conversation_history`) is a plain in-memory Python dict — it resets on every server restart and won't work across multiple worker processes.
  - `data/products.csv` is bundled but never read by any code path.

### Solution

- Built a Flask application factory (`app.py`) with blueprint-based routing (`routes/chat_routes.py`) and CORS enabled for cross-origin mobile/web clients.
- Implemented lightweight **intent detection** (`ChatbotService.detect_intent`) using keyword matching to classify messages into `order_query`, `crop_info`, `yield_query`, `pest_disease`, `soil_fertilizer`, or `general_query`.
- Added a **context-injection layer** (`get_app_data_context`) that, based on detected intent, pulls matching records from `AgricultureData` (crop details, order status) and relevant snippets from a static `AgricultureKnowledgeBase`, then appends them to the user's message before it reaches Gemini — a simple retrieval-augmentation pattern without a vector database.
- Wired the enriched prompt into Google's `google-generativeai` SDK (`models/gemini-pro-latest`), maintaining a per-`user_id` chat session so multi-turn context is preserved for the lifetime of the process.
- Exposed a broad REST surface beyond chat itself: crop lookup/search, order lookup by ID/user, quick-question suggestions, health check, and usage statistics — so a client app can build both a chatbot UI and structured crop/order screens off the same backend.
- Kept the codebase modular (`models/` for data access, `services/` for business logic, `routes/` for HTTP handling) so the Gemini integration, knowledge base, or data source can each be swapped independently.

### Impact

- A working, runnable chatbot API that answers agriculture questions with locally-grounded context (crop specifics, curated farming knowledge) rather than a raw LLM response, and can double as an order-tracking API for the same client app.
- Clear separation of concerns makes it straightforward to add features (e.g., swap `AgricultureData` for a real database, or add more intents) without touching the Flask routing layer.
- The `/api/statistics` and `/api/health` endpoints give an operator basic visibility into usage and service health without needing external tooling.
- Documented current limitations transparently in the README (no persistence, no auth, no tests) so downstream consumers know it is presently a prototype/MVP, not production-hardened.

### Lesson

- **Keep config validation error messages in sync with the variable actually being checked.** A mismatch here (`OPENAI_API_KEY` message vs. `GOOGLE_API_KEY` check) costs a developer real debugging time chasing the wrong `.env` entry — this should be fixed to reference `GOOGLE_API_KEY`.
- **Prune dependencies to what the runtime actually imports.** Carrying `langchain`, `chromadb`, `sentence-transformers`, and `openai` when only `google-generativeai` is used inflates install time and signals an architecture (vector-store RAG, OpenAI backend) that isn't what's actually running — either wire them in or remove them.
- **In-memory state is fine for a prototype but is a scaling and durability trap.** Any deployment beyond a single dev process (multiple gunicorn workers, autoscaling, restarts) will silently lose conversation history; this should move to Redis/SQLite before going further than local testing.
- **Bundling unused data files (`products.csv`) invites drift** between what's documented as "included" and what the API actually serves — either wire it into an endpoint or drop it from the bundled data.
- **A simple keyword-based intent classifier + static knowledge base is a pragmatic, low-cost way to ground an LLM** without standing up embeddings/vector search — a reasonable MVP choice, with a clear upgrade path to real retrieval if the knowledge base grows.

