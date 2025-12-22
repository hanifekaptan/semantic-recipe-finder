# Architecture

This document summarizes the high-level architecture, runtime data flow and operational runbook for the Semantic Recipe Finder project. It is intentionally concise — detailed implementation notes live in the code and MkDocs pages.

## Overview

- Purpose: provide fast semantic search over a recipe catalog and a lightweight frontend to browse results and recipe details.
- Two main components: a backend API (FastAPI) and a frontend UI (React + Vite).

## Components

- **Frontend (React + Vite)**
  - Single page application that issues search requests and renders result cards and a recipe detail modal.
  - Key pieces: `src/api` (API client), `src/hooks/useRecipes` (search + paging), UI components.

- **Backend (FastAPI)**
  - Routers: `app/api` (endpoints: `/search`, `/recipe/{id}`, `/health`).
  - Services: `app/services/SearchService` (vector search), `app/services/RecipeService` (card/detail assembly).
  - Models: Pydantic request/response models under `app/models`.
  - Core: `app/core/config.py` stores startup-loaded resources (embeddings, ids, model, dataframe).

- **Data & artifacts**
  - Raw CSV: `data/original/recipes.csv` (source dataset).
  - Processed artifacts: embeddings `data/processed/metadata_embeddings.npy`, ids `data/processed/ids_embeddings.npy`, master dataframe parquet `data/processed/master.parquet`.
  - Model: a sentence-transformers model (configured via `app.core.config.model_name`).

## Runtime data flow

1. Startup: backend loads embeddings, ids, transformer model and the master DataFrame. Resources are attached to `app.core.config` for global access.
2. User types a query in the frontend; frontend calls `POST /search` with JSON `{ "query": "..." }` and optional `offset`/`limit` query params.
3. `SearchService` encodes the query, computes similarity against stored embeddings (optionally via ANN), and returns an ordered list of (id, score) pairs.
4. Backend slices the ordered list by `offset`/`limit`, maps ids to lightweight recipe cards via `RecipeService`, and returns a paged response.
5. When a user opens a recipe, the frontend requests `GET /recipe/{id}` and receives the full recipe detail JSON.

## ASCII diagram

```
[User Browser]
    |
    v
[Frontend (React/Vite)]
    |
   HTTP
    v
[Backend (FastAPI)] ---> [SearchService: encode + similarity] ---> [Embeddings (npy) + IDs (npy)]
    |
    v
[RecipeService: build cards/details] ---> [Master DataFrame (parquet)]
```

## Useful commands

```bash
# Backend (development)
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Frontend (development)
cd frontend
npm install
npm run dev

# Run backend tests
cd backend
poetry run pytest -q
```

## Further reading

- See `docs/` for API details, quickstart and architecture notes with examples.
