# Semantic Recipe Finder

Description
-----------
Semantic Recipe Finder is a small full‑stack project that finds recipes using semantic natural language search. The backend (FastAPI + sentence-transformers) provides search and recipe data; the frontend (React + Vite + TypeScript) provides the user interface.

UI Preview
----------
![Main search](docs/assets/app.png)

![Recipe detail](docs/assets/modal.png)

Quickstart (local development)
------------------------------
1. Clone the repository and go to the project root.

2. Run the backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Set the backend URL in the frontend using the `VITE_API_BASE_URL` environment variable, or provide a fallback in `frontend/src/api/recipeService.ts`.

What it contains
----------------
- `backend/` — FastAPI API, embedding loader, search and recipe detail endpoints. API docs available at `GET /docs` (Swagger UI).
- `frontend/` — React + TypeScript + Vite app; `useRecipes` hook manages search and pagination; `recipeService` contains API helpers and mappers.
- `data/` — original and processed data (embeddings, metadata).
- `docs/` — MkDocs-based documentation content.

Project structure (summary)
---------------------------
Short tree view of key files and folders:

```
SemanticRecipeFinder/
├─ backend/
│  ├─ app/
│  │  ├─ api/            # endpoint definitions (search.py, health.py, ...)
│  │  ├─ core/           # config, middleware
│  │  ├─ models/         # pydantic models (SearchResponse, RecipeDetail)
│  │  ├─ services/       # SearchService, RecipeService
│  │  └─ main.py         # FastAPI application
│  ├─ data/              # original and processed data (embeddings, metadata)
│  └─ tests/             # unit & integration tests
├─ frontend/
│  ├─ src/
│  │  ├─ api/            # `recipeService.ts` (API calls, mappers)
│  │  ├─ components/     # React components (RecipeCard, Modal, ...)
│  │  ├─ hooks/          # custom hooks (`useRecipes`)
│  │  ├─ types/          # TS types and mapping helpers
│  │  └─ pages/          # page entry points
│  └─ public/            # static assets
├─ data/                 # global data folder (optional, also under backend)
├─ docs/                 # mkdocs content
├─ README.md
├─ mkdocs.yml
```

Endpoints
---------
- `GET /health` — health check
- `POST /search?offset={offset}&limit={limit}` — body `{ "query": "..." }`, returns a paged list of `{ recipe_id, similarity_score }`
- `GET /recipe/{id}` — recipe detail

Tests
-----
- Backend tests are in `backend/tests`:

```bash
cd backend
poetry run pytest -q
```

- Frontend integration tests (if present) can be run under `frontend` (e.g. `npm run test`).

Configuration & environment
---------------------------
- Frontend: Vite exposes environment variables prefixed with `VITE_` (e.g. `VITE_API_BASE_URL`).
- Backend: environment variables and defaults are configured in `backend/app/core/config.py`.

Contact
-------
For questions: hanifekaptan.dev@gmail.com

