# System Architecture

This document describes the architecture, design decisions, and data flow of the Semantic Recipe Finder application.

## 🏗️ High-Level Architecture

```
┌──────────────┐         ┌──────────────┐
│   Streamlit  │◄───────►│   FastAPI    │
│   Frontend   │  HTTP   │   Backend    │
└──────────────┘         └──────┬───────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌─────────┐ ┌─────────┐ ┌──────────┐
              │ ChromaDB│ │DataFrame│ │  Model  │
              │ Vector  │ │ Recipe  │ │sentence │
              │  Store  │ │  Data   │ │transform│
              └─────────┘ └─────────┘ └─────────┘
```

## 📦 Component Overview

### Frontend (Streamlit)

!!! info "Purpose"
    User-facing interface for recipe search and browsing

!!! abstract "Technology Stack"
    Streamlit 1.41.1 with component-based architecture

**Key Components**:

=== "Search Bar"
    `search_bar.py` - Query input with real-time validation
    
=== "Recipe Card"
    `recipe_card.py` - Compact recipe display for search results
    
=== "Recipe Detail"
    `recipe_detail.py` - Full recipe view with ingredients and instructions
    
=== "Header"
    `header.py` - App navigation and branding

**State Management**:
- Uses Streamlit session state for search results caching
- Maintains navigation state between search and detail views
- API client handles backend communication with error handling

**Communication**:
- HTTP client (`httpx`) for API requests
- Configurable backend URL via `API_BASE_URL` environment variable
- Error handling with user-friendly messages

### Backend (FastAPI)

!!! success "Purpose"
    RESTful API providing semantic search and recipe data

!!! abstract "Technology Stack"
    FastAPI 0.115.6 with async support

**Architecture Layers**:

=== "🌐 API Layer"
    **Location**: `app/api/`
    
    - `health.py` - Health check endpoint
    - `search.py` - Semantic search endpoint with pagination
    - `routes.py` - Recipe detail retrieval

=== "⚙️ Service Layer"
    **Location**: `app/services/`
    
    - `search_service.py` - Search orchestration and result building
    - `detail_service.py` - Recipe detail retrieval from DataFrame
    - `vectorstore.py` - ChromaDB operations and vector search
    - `loading_service.py` - Startup data and model loading

=== "📋 Model Layer"
    **Location**: `app/models/`
    
    - Pydantic models for request/response validation
    - Type safety and automatic API documentation
    - Models: `RecipeCard`, `RecipeDetail`, `SearchQuery`, `SearchResponse`

=== "🔧 Utility Layer"
    **Location**: `app/utils/`
    
    - `data_preprocessor.py` - Text cleaning (lowercase, remove digits/punctuation)
    - `vectorizer.py` - Text-to-vector conversion with normalization

### Vector Database (ChromaDB)

!!! tip "Purpose"
    Efficient similarity search on recipe embeddings

!!! abstract "Technology Stack"
    ChromaDB 0.5.23 with DuckDB+Parquet backend

???+ info "Configuration Details"
    - **Dimension**: 384 (from `all-MiniLM-L6-v2` model)
    - **Distance Metric**: Cosine similarity (default)
    - **Persistence**: `data/processed/persist/` directory
    - **Collection**: Single `recipes` collection with 100 embeddings

**Key Operations**:

=== "Initialize"
    `load_or_build_collection()` - Initialize or load existing collection
    
=== "Search"
    `search_collection(query_vector, top_k)` - Vector similarity search
    
=== "Normalize"
    Automatic normalization of query vectors for consistent results

### Machine Learning Model

!!! example "Model"
    `sentence-transformers/all-MiniLM-L6-v2`

???+ abstract "Specifications"
    - **Architecture**: MiniLM (distilled BERT)
    - **Output**: 384-dimensional dense vectors
    - **Training**: Trained on 1B+ sentence pairs
    - **Performance**: ~120M parameters, fast inference (~50ms per query)
    - **Use Case**: Optimized for semantic similarity tasks

!!! success "Why This Model?"
    ✅ Small size (90MB) suitable for CPU inference  
    ✅ Good balance between speed and quality  
    ✅ Widely used and well-documented  
    ✅ No GPU required for production deployment

## 🔄 Data Flow

### Search Request Flow

=== "1️⃣ User Input"
    ```
    User enters: "quick vegetarian pasta"
    ```

=== "2️⃣ Frontend Processing"
    - Streamlit validates input (non-empty)
    - Sends POST request to `/search` endpoint
    - Includes pagination params (offset, limit)

=== "3️⃣ Backend API Layer"
    - FastAPI receives request
    - Validates with `SearchQuery` Pydantic model
    - Passes to `SearchService`

=== "4️⃣ Service Layer Processing"
    ```python
    # search_service.py
    1. Clean query text (remove special chars, lowercase)
    2. Vectorize with sentence-transformers model
    3. Normalize vector (L2 norm)
    4. Call ChromaDB for similarity search (top 100)
    5. Retrieve recipe data from DataFrame
    6. Build RecipeCard objects
    7. Apply pagination (offset/limit)
    8. Return SearchResponse
    ```

=== "5️⃣ Vector Search"
    ```python
    # vectorstore.py
    1. Receive 384-dim query vector
    2. Query ChromaDB collection
    3. ChromaDB computes cosine similarity with all 100 vectors
    4. Return top_k recipe IDs and similarity scores
    ```

=== "6️⃣ Recipe Data Retrieval"
    ```python
    # search_service.py -> get_recipe_cards()
    1. Receive list of recipe IDs from ChromaDB
    2. Lookup each ID in pandas DataFrame
    3. Extract required fields for RecipeCard
    4. Handle missing/invalid IDs gracefully
    5. Return list of RecipeCard objects
    ```

=== "7️⃣ Frontend Rendering"
    - Receive paginated results
    - Display recipe cards in grid layout
    - Show similarity scores
    - Enable click-through to detail view

### Recipe Detail Flow

=== "1️⃣ User Action"
    User clicks recipe card

=== "2️⃣ Navigation"
    Frontend navigates to detail page with `recipe_id`

=== "3️⃣ API Request"
    GET request to `/recipe/{recipe_id}`

=== "4️⃣ Data Retrieval"
    `DetailService` retrieves full recipe from DataFrame

=== "5️⃣ Response"
    Returns `RecipeDetail` with all fields

=== "6️⃣ Render"
    Frontend renders detailed view

## 🗄️ Data Storage

=== "📊 Recipe DataFrame"
    !!! info "Format"
        Pandas DataFrame loaded from `recipes.csv`

    !!! abstract "Index"
        `recipe_id` (integer)

    ???+ note "Columns (subset used)"
        - `name`, `description`, `recipe_category`
        - `keywords` (list), `ingredients` (list), `instructions` (list)
        - `n_ingredients`, `total_time_minutes`
        - `calories`, `fat_content`, `protein_content`, `carbohydrate_content`
        - `aggregated_rating`

    !!! tip "Access Pattern"
        ✅ Loaded once at startup  
        ✅ Stored in `config.df` for global access  
        ✅ Indexed access by `recipe_id` (O(1) lookup)

=== "🔢 Embeddings Storage"
    !!! abstract "Files"
        - `ids_embs.npy` - Recipe IDs (1D array)
        - `metadata_embs.npy` - Embeddings (2D array, shape: [100, 384])

    ???+ info "Loading Process"
        1. Read at startup by `loading_service.py`
        2. Inserted into ChromaDB collection
        3. Used for vector similarity search

    ???+ success "Pre-computation Details"
        - Embeddings pre-computed offline (see `notebooks/vectorize.py`)
        - Combines: name + description + category + keywords
        - Normalized to unit length

## 🔧 Configuration

=== "⚙️ Global Config"
    !!! abstract "Location: `app/core/config.py`"
        Singleton pattern for application state

    ```python
    class Config:
        ready: bool = False           # App initialization status
        model: SentenceTransformer    # Loaded ML model
        df: pd.DataFrame              # Recipe data
        search_service: SearchService # Initialized service
        detail_service: DetailService # Initialized service
    ```

=== "🚀 Startup Sequence"
    !!! abstract "Location: `app/main.py`"
        Application initialization workflow

    ```python
    @app.on_event("startup")
    async def startup_event():
        1. Load sentence-transformer model
        2. Load recipe DataFrame from CSV
        3. Initialize ChromaDB collection
        4. Load pre-computed embeddings
        5. Initialize services
        6. Set config.ready = True
    ```

## 🧪 Testing Architecture

???+ abstract "Test Structure"
    ```
    tests/
    ├── integration/
    │   └── test_smoke_api.py        # Full API testing (15 tests)
    └── unit/
        ├── services/
        │   ├── test_search_service.py    # SearchService (21 tests)
        │   └── test_detail_service.py    # DetailService (7 tests)
        └── utils/
            ├── test_preprocessor_new.py  # Text cleaning (13 tests)
            └── test_vectorizer_new.py    # Vectorization (7 tests)
    ```

=== "🔌 Integration Tests"
    - Mock `search_collection()` to avoid ChromaDB dependency
    - Use `FastAPI.TestClient` for HTTP request simulation
    - Mock model with 384-dim vectors

=== "🧩 Unit Tests"
    - Mock external dependencies (model, ChromaDB)
    - Test edge cases (empty queries, missing data)
    - Verify error handling and fallback logic

!!! success "Coverage Summary"
    - **Total Tests**: 61
    - **Pass Rate**: 100% ✅
    - **Coverage Areas**:
        - API endpoints (health, search, detail)
        - Service layer logic
        - Text preprocessing
        - Vector operations
        - Error handling

## 🚀 Performance Considerations

=== "⚡ Backend Optimization"
    !!! tip "Startup Loading"
        ✅ All data loaded once at startup  
        ✅ Models cached in memory  
        ✅ No per-request model loading

    !!! tip "Vector Search"
        ✅ ChromaDB uses efficient indexing  
        ✅ Pre-normalized embeddings  
        ✅ Fast cosine similarity computation

    !!! tip "DataFrame Access"
        ✅ Indexed by recipe_id for O(1) lookup  
        ✅ Minimal memory footprint (100 recipes)  
        ✅ No database queries needed

=== "📈 Scalability"
    !!! info "Current Scale"
        100 recipes (proof-of-concept)

    ???+ example "To Scale Up"
        - 🔼 Increase ChromaDB collection size
        - 📦 Add batch processing for embeddings
        - 💾 Consider caching layer (Redis)
        - ⚖️ Deploy with load balancer
        - 🎮 Use GPU for model inference at scale

## 🔒 Security

!!! warning "Security Considerations"
    ⚠️ No authentication (demo application)  
    ✅ Input validation with Pydantic  
    ✅ CORS enabled for frontend communication  
    ✅ No user data storage  
    ✅ Static dataset (no user-generated content)

## 📝 Design Decisions

=== "🗄️ ChromaDB"
    !!! question "Why ChromaDB?"
        ✅ Easy setup with minimal configuration  
        ✅ Supports persistent storage out-of-the-box  
        ✅ Good performance for <10k vectors  
        ✅ Python-native with good documentation

=== "🤖 Sentence-Transformers"
    !!! question "Why Sentence-Transformers?"
        ✅ State-of-the-art semantic similarity  
        ✅ Easy integration with HuggingFace  
        ✅ No API keys or external services needed  
        ✅ Fast inference on CPU

=== "🎨 Streamlit"
    !!! question "Why Streamlit?"
        ✅ Rapid prototyping for ML/AI apps  
        ✅ Built-in state management  
        ✅ Easy deployment to Spaces  
        ✅ Component-based architecture

=== "⚡ FastAPI"
    !!! question "Why FastAPI?"
        ✅ Modern async Python framework  
        ✅ Automatic OpenAPI documentation  
        ✅ Type safety with Pydantic  
        ✅ High performance (comparable to Node.js)

---

**Navigation**: [Home](index.md) | [Architecture](architecture.md) | [API](api.md)
