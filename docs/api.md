# API Usage

This document summarizes the backend API endpoints provided by the FastAPI service. Use the interactive OpenAPI docs at `http://localhost:8000/docs` for more details and try-it-out requests.

Base URL
--------
Assuming the backend runs locally during development, the base URL is:

```
http://127.0.0.1:8000
```

OpenAPI/Swagger UI
------------------
- OpenAPI JSON: `/openapi.json` (e.g. `http://127.0.0.1:8000/openapi.json`)
- Swagger UI: `/docs`
- ReDoc: `/redoc`

Common response conventions
---------------------------
- Successful responses use HTTP 200 with application/json.
- Errors use appropriate 4xx/5xx status codes and a JSON body with `detail` when raised by FastAPI `HTTPException`.

Endpoints
---------

1) Health

GET /health

Purpose: simple liveness/readiness probe.

Response (200):

```json
{ "status": "ok" }
```

2) Search (semantic)

POST /search?offset={offset}&limit={limit}

Description: Runs a semantic search for the provided query string and returns a batch (slice) of results indicated by `offset` and `limit`.

Request body (JSON):

```json
{ "query": "pasta with tomato" }
```

Query parameters:
- `offset` (int, default 0): zero-based index to start the batch from.
- `limit` (int, default 20): number of items to return in this batch (max limited by server).

Response (200):

```json
{
	"search_results": [
		{ "recipe_id": 123, "similarity_score": 0.9123 },
		{ "recipe_id": 456, "similarity_score": 0.8976 }
	],
	"total_count": 120,
	"offset": 0,
	"limit": 20
}
```

Notes:
- The backend may internally compute a larger top-k result list and slice it by `offset`/`limit` to provide stable paging. Clients should rely on `total_count` to know when no more results exist.
- The request is POST to allow more complex search payloads in the future (filters, facets).

3) Recipe detail

GET /recipe/{recipe_id}

Description: Return the full recipe metadata and content for the given integer `recipe_id`.

Path parameter:
- `recipe_id` (int) — identifier of the recipe to fetch.

Response (200): a `RecipeDetail` JSON object. Key fields (abridged):
- `recipe_id` (int)
- `name` (string)
- `description` (string | null)
- `ingredients` (array[string])
- `recipe_instructions` (string | null)
- `total_time_minutes` (int | null)
- `n_ingredients` (int | null)
- `calories` (number | null)
- `aggregated_rating` (number | null)
- `keywords` (array[string])
- nutrition fields (e.g. `fat_content`, `protein_content`) are returned as strings or `null` for consistency with Pydantic model.

Example response (200, abridged):

```json
{
	"recipe_id": 123,
	"name": "Tomato Pasta",
	"description": "Simple tomato pasta",
	"ingredients": ["pasta", "tomato", "olive oil"],
	"recipe_instructions": "Boil pasta. Prepare sauce...",
	"total_time_minutes": 30,
	"n_ingredients": 3,
	"calories": 420,
	"aggregated_rating": 4.5,
	"keywords": ["easy", "vegetarian"],
	"fat_content": "12.34",
	"protein_content": "8.50",
	"sugar_content": "4.20",
	"carbohydrate_content": "60.00"
}
```

Errors:
- `404 Not Found` — returned when `recipe_id` is not present or the row is malformed.
- `500 Internal Server Error` — returned if backend data resources (DataFrame, embeddings, etc.) are not initialized.

Error cases
-----------
- If the server-side search resources are not initialized, `/search` will return HTTP 500 with a descriptive message.
- If a requested `recipe_id` is not present in the dataset, `/recipe/{recipe_id}` returns HTTP 404.

Examples (curl)
---------------

# Health
```bash
curl -sS http://127.0.0.1:8000/health
```

# POST search: first 20 results
```bash
curl -sS -X POST 'http://127.0.0.1:8000/search?offset=0&limit=20' -H 'Content-Type: application/json' -d '{"query":"chocolate cake"}'
```

# Recipe detail
```bash
curl -sS http://127.0.0.1:8000/recipe/123
```

See the interactive Swagger UI at `/docs` for request/response models and try-it-out execution.
