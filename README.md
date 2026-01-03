# Semantic Recipe Finder

**Semantic Recipe Finder** is a full-stack application that uses natural language semantic search to find recipes. Built with FastAPI backend and Streamlit frontend, it leverages sentence-transformers and ChromaDB for intelligent recipe discovery.

## 🌐 Links

- **Live Demo**: [HuggingFace Spaces](https://huggingface.co/spaces/hanifekaptan/semantic-recipe-finder) _(coming soon)_
- **Documentation**: [GitHub Pages](https://hanifekaptan.github.io/semantic-recipe-finder/) _(coming soon)_
- **Repository**: [GitHub](https://github.com/hanifekaptan/semantic-recipe-finder)

## ✨ Features

- **Semantic Search**: Natural language queries powered by sentence-transformers (all-MiniLM-L6-v2)
- **Fast Vector Search**: ChromaDB with 384-dimensional embeddings for efficient similarity search
- **RESTful API**: FastAPI backend with comprehensive endpoints and OpenAPI documentation
- **Modern UI**: Streamlit frontend with responsive recipe cards and detailed views
- **Comprehensive Tests**: 61 unit and integration tests with pytest
- **Docker Ready**: Multi-container setup with docker-compose for easy deployment

## 🚀 Quickstart (local development)

### Prerequisites
- Python 3.10

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/hanifekaptan/semantic-recipe-finder.git
cd semantic-recipe-finder
```

2. **Create and activate virtual environment**
```powershell
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Run the backend (FastAPI)**
```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

5. **Run the frontend (Streamlit)** _(in a new terminal)_
```powershell
streamlit run frontend/app.py --server.port 8501
```
The UI will be available at `http://localhost:8501`.

### Environment Variables
- `API_BASE_URL`: Backend URL for Streamlit frontend (default: `http://localhost:8000`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## 📂 Project Structure

```
semantic-recipe-finder/
├── app/                          # FastAPI backend application
│   ├── api/                      # API routes and endpoints
│   │   ├── health.py            # Health check endpoint
│   │   ├── routes.py            # Recipe detail endpoint
│   │   └── search.py            # Search endpoint
│   ├── core/                     # Core configuration and utilities
│   │   ├── config.py            # Global configuration and state
│   │   └── logging.py           # Logging setup
│   ├── models/                   # Pydantic data models
│   │   ├── recipe_card.py       # Recipe card model (search results)
│   │   ├── recipe_detail.py     # Full recipe detail model
│   │   ├── search_query.py      # Search request model
│   │   └── search_response.py   # Search response model
│   ├── services/                 # Business logic services
│   │   ├── detail_service.py    # Recipe detail retrieval
│   │   ├── loading_service.py   # Data and model loading
│   │   ├── search_service.py    # Semantic search logic
│   │   └── vectorstore.py       # ChromaDB operations
│   ├── utils/                    # Utility functions
│   │   ├── data_preprocessor.py # Text cleaning
│   │   └── vectorizer.py        # Text vectorization
│   └── main.py                   # FastAPI app initialization
├── frontend/                     # Streamlit frontend application
│   ├── api/
│   │   └── client.py            # Backend API client
│   ├── components/               # Reusable UI components
│   │   ├── header.py            # App header
│   │   ├── recipe_card.py       # Recipe card display
│   │   ├── recipe_detail.py     # Detailed recipe view
│   │   └── search_bar.py        # Search input
│   ├── pages/                    # Streamlit pages
│   │   ├── detail.py            # Recipe detail page
│   │   └── search.py            # Search results page
│   ├── utils/
│   │   └── utility.py           # Helper functions
│   └── app.py                    # Streamlit app entrypoint
├── data/                         # Data storage
│   ├── raw/
│   │   └── recipes.csv          # Original recipe dataset
│   └── processed/
│       ├── ids_embs.npy         # Recipe IDs
│       ├── metadata_embs.npy    # Recipe metadata embeddings
│       └── persist/             # ChromaDB persistent storage
├── docker/                       # Docker configurations
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── entrypoint.sh
├── tests/                        # Test suite
│   ├── integration/             # API integration tests
│   │   └── test_smoke_api.py
│   └── unit/                     # Unit tests
│       ├── services/            # Service layer tests
│       └── utils/               # Utility tests
├── docker-compose.yml            # Multi-container orchestration
├── Dockerfile                    # HuggingFace Space Dockerfile
├── requirements.txt              # Python dependencies
└── pytest.ini                    # Pytest configuration
```

## 🏗️ Architecture Overview

### Backend (FastAPI)
- **Semantic Search**: Uses `all-MiniLM-L6-v2` sentence-transformer model for query encoding
- **Vector Database**: ChromaDB with DuckDB+Parquet backend for 100 recipe embeddings (384 dimensions)
- **Service Layer**: Clean separation between API routes, business logic, and data access
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes
- **API Documentation**: Auto-generated OpenAPI (Swagger) docs at `/docs`

### Frontend (Streamlit)
- **Component-Based**: Modular UI components for search, cards, and detail views
- **API Client**: HTTP client with error handling for backend communication
- **Session State**: Manages search results and navigation state
- **Responsive Design**: Clean, user-friendly interface optimized for recipe browsing

### Data Flow
1. User enters natural language query in Streamlit UI
2. Frontend sends request to `/search` endpoint
3. Backend cleans and vectorizes query text
4. ChromaDB performs similarity search on recipe embeddings
5. Top 100 results retrieved from DataFrame
6. Results paginated and returned to frontend
7. Frontend displays recipe cards with key information

## 🧪 Testing

The project includes comprehensive test coverage with pytest:

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=frontend

# Run specific test suite
pytest tests/unit/services/
pytest tests/integration/
```

**Test Statistics**:
- 61 total tests (28 service tests, 18 utility tests, 15 integration tests)
- Unit tests: Mock-based testing for services and utilities
- Integration tests: FastAPI TestClient for full API testing
- All tests passing with proper fixtures and parametrization

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```
This starts both backend (port 8000) and frontend (port 8501) containers.

### Individual Containers
```bash
# Backend only
docker build -f docker/backend.Dockerfile -t recipe-finder-backend .
docker run -p 8000:8000 recipe-finder-backend

# Frontend only
docker build -f docker/frontend.Dockerfile -t recipe-finder-frontend .
docker run -p 8501:8501 recipe-finder-frontend
```

### HuggingFace Spaces
The root `Dockerfile` is configured for HuggingFace Spaces deployment with both services.

## 📊 Dataset

The application uses a subset of recipe data with:
- **100 recipes** from Food.com dataset
- **Metadata**: Name, description, category, ingredients, nutrition facts, ratings
- **Embeddings**: Pre-computed 384-dimensional vectors from recipe metadata
- **Storage**: ChromaDB persistent storage at `data/processed/persist/`

## 🛠️ Technology Stack

**Backend**:
- FastAPI 0.115.6
- sentence-transformers (all-MiniLM-L6-v2)
- ChromaDB 0.5.23
- Pandas, NumPy
- Pydantic for data validation

**Frontend**:
- Streamlit 1.41.1
- httpx for API calls
- Python 3.10+

**Testing**:
- pytest 9.0.2
- pytest-asyncio
- unittest.mock

**DevOps**:
- Docker & docker-compose
- GitHub Actions _(coming soon)_
- HuggingFace Spaces deployment

## 📝 API Endpoints

### `GET /health`
Health check endpoint for monitoring.

**Response**: `{ "status": "ok", "ready": true }`

### `POST /search`
Semantic search for recipes.

**Request Body**:
```json
{
  "query": "quick pasta dinner",
  "offset": 0,
  "limit": 20
}
```

**Response**:
```json
{
  "search_results": [
    {
      "recipe_id": 123,
      "similarity_score": 0.87,
      "card": {
        "recipe_id": 123,
        "name": "Quick Pasta Carbonara",
        "description": "Creamy pasta dish...",
        "recipe_category": "Main Course",
        "keywords": ["pasta", "quick", "italian"],
        "n_ingredients": 5,
        "total_time_minutes": 20,
        "calories": 450.0,
        "aggregated_rating": 4.5
      }
    }
  ],
  "total_results": 42,
  "offset": 0,
  "limit": 20
}
```

### `GET /recipe/{recipe_id}`
Get full recipe details.

**Response**:
```json
{
  "recipe_id": 123,
  "name": "Quick Pasta Carbonara",
  "description": "Creamy pasta dish...",
  "recipe_category": "Main Course",
  "keywords": ["pasta", "quick", "italian"],
  "ingredients": ["spaghetti", "eggs", "bacon", "parmesan", "pepper"],
  "instructions": ["Step 1...", "Step 2..."],
  "n_ingredients": 5,
  "total_time_minutes": 20,
  "calories": 450.0,
  "fat_content": 15.0,
  "protein_content": 25.0,
  "aggregated_rating": 4.5
}
```

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## 📧 Contact

Hanife Kaptan - [hanifekaptan.dev@gmail.com](mailto:hanifekaptan.dev@gmail.com)

Project Link: [https://github.com/hanifekaptan/semantic-recipe-finder](https://github.com/hanifekaptan/semantic-recipe-finder)

---

⭐ Star this repo if you find it helpful!