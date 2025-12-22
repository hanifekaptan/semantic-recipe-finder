# Quickstart (Local development)

This document provides step-by-step instructions to run the project locally for development. It covers both backend and frontend services.

Prerequisites
-------------
- Git
- Python 3.11+
- npm (or pnpm/yarn)
- Poetry (recommended) for the backend

1) Clone the repository

```bash
git clone <https://github.com/hanifekaptan/semantic-recipe-finder.git>
cd semantic-recipe-finder
```

2) Backend setup and run

```bash
cd backend
poetry install
# Run development server with automatic reload
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Notes:
- If you prefer to use a virtualenv + pip, install dependencies from `pyproject.toml` accordingly.
- The backend loads sample test assets by default (see `backend/app/core/config.py`). Replace those paths when using real data.

3) Frontend setup and run

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server typically serves at `http://localhost:5173` — check terminal output.

4) Verify both services

- API health check:

```bash
curl http://127.0.0.1:8000/health
```

- Open the frontend app in your browser (Vite URL). The frontend calls the backend at `http://localhost:8000` by default.

Optional: Build for production
-----------------------------
- Backend: package according to your cloud provider; run `uvicorn app.main:app` (no `--reload`) in a production process manager.
- Frontend: build static assets and serve with a CDN or static web server:

```bash
cd frontend
npm run build
```

Notes on environment variables
------------------------------
- `CORS_ALLOWED_ORIGINS`: set this (comma-separated or JSON array) in production to allow frontend origin(s).
- Other config values are in `backend/app/core/config.py` and can be made environment-driven if desired.

Troubleshooting
---------------
- If the backend fails to start due to missing model files, ensure paths in `config.py` point to valid files or provide smaller test assets.
- If the frontend cannot reach the API, confirm `VITE_API_BASE` in `frontend/.env` (or `import.meta.env`) matches the backend base URL.

That's it — with both servers running you can develop and test the full stack locally.
