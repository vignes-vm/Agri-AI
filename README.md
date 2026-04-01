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

## License

Add your preferred license here (for example, MIT).
