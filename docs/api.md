# API Reference

!!! abstract "Overview"
    Complete API documentation for the Semantic Recipe Finder backend.

## 🌐 Base URL

=== "Development"
    ```
    http://localhost:8000
    ```

=== "Production"
    ```
    https://semantic-recipe-finder.hf.space
    ```
    *HuggingFace Spaces deployment*

## 📚 Interactive Documentation

!!! tip "FastAPI Auto-Generated Docs"
    FastAPI provides interactive API documentation:
    
    - 📖 **Swagger UI**: `{BASE_URL}/docs`
    - 📘 **ReDoc**: `{BASE_URL}/redoc`
    - 📄 **OpenAPI Schema**: `{BASE_URL}/openapi.json`

## 🔓 Authentication

!!! info "Public Access"
    No authentication required (public demo application).

---

## 🔌 Endpoints

### Health Check

!!! abstract "Endpoint"
    `GET /health`

!!! info "Description"
    Check if the backend is ready to serve requests.

=== "Request"
    **No parameters required**

=== "Response: 200 OK"
    ```json
    {
      "status": "ok",
      "ready": true
    }
    ```
    
    **Response Fields**:
    
    - `status` (string): Health status indicator ("ok" or "error")
    - `ready` (boolean): Whether all services are initialized

=== "Example"
    ```bash
    curl http://localhost:8000/health
    ```
    
    **Response**:
    ```json
    {
      "status": "ok",
      "ready": true
    }
    ```

---

### Search Recipes

!!! abstract "Endpoint"
    `POST /search`

!!! info "Description"
    Perform semantic search on recipes using natural language queries.

=== "📥 Request"
    **Content-Type**: `application/json`
    
    ```json
    {
      "query": "string",
      "offset": 0,
      "limit": 20
    }
    ```
    
    **Request Fields**:
    
    - `query` (string, **required**): Natural language search query
        - Example: "quick pasta dinner"
        - Example: "healthy vegetarian meal"
        - Example: "chocolate dessert under 30 minutes"
    - `offset` (integer, optional): Number of results to skip (default: 0)
    - `limit` (integer, optional): Maximum results per page (default: 20, max: 100)

=== "📤 Response: 200 OK"
    ```json
    {
      "search_results": [
        {
          "recipe_id": 123,
          "similarity_score": 0.87,
          "card": {
            "recipe_id": 123,
            "name": "Quick Pasta Carbonara",
            "description": "Creamy Italian pasta with eggs and bacon",
            "recipe_category": "Main Course",
            "keywords": ["pasta", "italian", "quick", "comfort-food"],
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
    
    **Response Fields**:
    
    - `search_results` (array): List of search result objects
        - `recipe_id` (integer): Unique recipe identifier
        - `similarity_score` (float): Cosine similarity score (0-1, higher is better)
        - `card` (object): Recipe card data
    - `total_results` (integer): Total matching recipes (before pagination)
    - `offset` (integer): Current offset
    - `limit` (integer): Current limit

=== "❌ Error Responses"
    **422 Unprocessable Entity** - Invalid request body
    
    ```json
    {
      "detail": [
        {
          "loc": ["body", "query"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```
    
    **500 Internal Server Error** - Search execution failed
    
    ```json
    {
      "detail": "Search execution failed"
    }
    ```

=== "💡 Examples"
    **Basic Search**:
    ```bash
    curl -X POST http://localhost:8000/search \
      -H "Content-Type: application/json" \
      -d '{"query": "pasta"}'
    ```
    
    **Paginated Search**:
    ```bash
    curl -X POST http://localhost:8000/search \
      -H "Content-Type: application/json" \
      -d '{
        "query": "vegetarian dinner",
        "offset": 0,
        "limit": 10
      }'
    ```
    
    **Python Example**:
    ```python
    import httpx

    response = httpx.post(
        "http://localhost:8000/search",
        json={
            "query": "quick healthy breakfast",
            "offset": 0,
            "limit": 20
        }
    )

    data = response.json()
    for result in data["search_results"]:
        print(f"{result['card']['name']}: {result['similarity_score']:.2f}")
    ```

---

### Get Recipe Detail

!!! abstract "Endpoint"
    `GET /recipe/{recipe_id}`

!!! info "Description"
    Retrieve full details for a specific recipe.

=== "📥 Request"
    **Path Parameters**:
    
    - `recipe_id` (integer, **required**): Unique recipe identifier

=== "📤 Response: 200 OK"
    ```json
    {
      "recipe_id": 123,
      "name": "Quick Pasta Carbonara",
      "description": "Creamy Italian pasta with eggs and bacon",
      "recipe_category": "Main Course",
      "keywords": ["pasta", "italian", "quick", "comfort-food"],
      "ingredients": [
        "200g spaghetti",
        "100g bacon",
        "2 eggs",
        "50g parmesan cheese",
        "black pepper to taste"
      ],
      "instructions": [
        "Cook spaghetti according to package directions",
        "Fry bacon until crispy",
        "Beat eggs with parmesan cheese",
        "Drain pasta and mix with bacon",
        "Remove from heat and stir in egg mixture",
        "Season with black pepper and serve"
      ],
      "n_ingredients": 5,
      "total_time_minutes": 20,
      "calories": 450.0,
      "fat_content": 18.0,
      "protein_content": 22.0,
      "sugar_content": 2.0,
      "carbohydrate_content": 55.0,
      "aggregated_rating": 4.5,
      "fat_content_perc": 28.0,
      "protein_content_perc": 34.0,
      "sugar_content_perc": 3.0,
      "carbohydrate_content_perc": 85.0
    }
    ```
    
    ???+ note "Response Fields"
        - `recipe_id`, `name`, `description`, `recipe_category`
        - `keywords`, `ingredients`, `instructions`
        - `n_ingredients`, `total_time_minutes`
        - `calories`, `fat_content`, `protein_content`, `sugar_content`, `carbohydrate_content`
        - `aggregated_rating`

=== "❌ Error: 404 Not Found"
    ```json
    {
      "detail": "Recipe not found"
    }
    ```

=== "💡 Examples"
    **Basic Request**:
    ```bash
    curl http://localhost:8000/recipe/123
    ```
    
    **Python Example**:
    ```python
    import httpx

    recipe_id = 123
    response = httpx.get(f"http://localhost:8000/recipe/{recipe_id}")

    if response.status_code == 200:
        recipe = response.json()
        print(f"Recipe: {recipe['name']}")
        print(f"Ingredients: {len(recipe['ingredients'])}")
        print(f"Steps: {len(recipe['instructions'])}")
    elif response.status_code == 404:
        print("Recipe not found")
    ```

---

## 📋 Data Models

???+ example "SearchQuery"
    Request model for search endpoint.
    
    ```python
    class SearchQuery(BaseModel):
        query: str
        offset: int = 0
        limit: int = 20
    ```

???+ example "RecipeCard"
    Compact recipe information for search results.
    
    ```python
    class RecipeCard(BaseModel):
        recipe_id: int
        name: Optional[str] = None
        description: Optional[str] = None
        recipe_category: Optional[str] = None
        keywords: List[str] = []
        n_ingredients: Optional[int] = None
        total_time_minutes: Optional[int] = None
        calories: Optional[float] = None
        aggregated_rating: Optional[float] = None
    ```

???+ example "SearchResult"
    Single search result with similarity score.
    
    ```python
    class SearchResult(BaseModel):
        recipe_id: int
        similarity_score: float
        card: RecipeCard
    ```

???+ example "SearchResponse"
    Complete search response with pagination.
    
    ```python
    class SearchResponse(BaseModel):
        search_results: List[SearchResult]
        total_results: int
        offset: int
        limit: int
    ```

???+ example "RecipeDetail"
    Full recipe information.
    
    ```python
    class RecipeDetail(BaseModel):
        recipe_id: int
        name: Optional[str] = None
        description: Optional[str] = None
        recipe_category: Optional[str] = None
        keywords: List[str] = []
        ingredients: List[str] = []
        instructions: List[str] = []
        n_ingredients: Optional[int] = None
        total_time_minutes: Optional[int] = None
        calories: Optional[float] = None
        fat_content: Optional[float] = None
        protein_content: Optional[float] = None
        sugar_content: Optional[float] = None
        carbohydrate_content: Optional[float] = None
        fat_content_perc: Optional[float] = None
        protein_content_perc: Optional[float] = None
        sugar_content_perc: Optional[float] = None
        carbohydrate_content_perc: Optional[float] = None
    ```

---

## 💡 Query Examples

!!! tip "Natural Language Understanding"
    The semantic search understands context and synonyms:

=== "🍝 Cuisine-based"
    - "Italian pasta dishes"
    - "Mexican tacos"
    - "Asian stir fry"

=== "🥗 Dietary"
    - "vegetarian dinner"
    - "low carb breakfast"
    - "high protein snack"

=== "⏱️ Time-based"
    - "quick 15 minute meal"
    - "slow cooker recipes"
    - "make ahead desserts"

=== "🥕 Ingredient-based"
    - "chicken breast recipes"
    - "uses tomatoes"
    - "chocolate desserts"

=== "🍽️ Meal type"
    - "breakfast ideas"
    - "lunch for work"
    - "dinner party main course"

=== "👨‍🍳 Cooking style"
    - "baked chicken"
    - "grilled vegetables"
    - "no bake desserts"

=== "🔗 Combined queries"
    - "quick healthy vegetarian dinner"
    - "easy chicken pasta under 30 minutes"
    - "low carb high protein breakfast"

---

## ⚡ Rate Limiting

!!! warning "Current Status"
    No rate limiting implemented (demo application).

???+ tip "Production Recommendations"
    - Rate limiting per IP
    - API key authentication
    - Request throttling

---

## 🌐 CORS Configuration

!!! info "Current Configuration"
    CORS is enabled for all origins in development.

???+ example "Production Setup"
    Restrict to specific domains:
    
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://your-frontend-domain.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```

---

## ⚠️ Error Handling

!!! abstract "HTTP Status Codes"
    All endpoints return standard HTTP status codes:

| Status | Meaning |
|--------|--------|
| `200 OK` | ✅ Successful request |
| `404 Not Found` | ❌ Resource not found |
| `422 Unprocessable Entity` | ⚠️ Validation error |
| `500 Internal Server Error` | 🔥 Server error |

!!! note "Error Response Format"
    Error responses include a `detail` field with error description.

---

**Navigation**: [Home](index.md) | [Architecture](architecture.md) | [API](api.md)
