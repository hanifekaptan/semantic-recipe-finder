"""Centralized middleware helpers (CORS) for the app.

This module is written with Render deployment in mind: prefer setting
allowed origins via the `CORS_ALLOWED_ORIGINS` environment variable
(comma-separated or JSON array). If no env var is present the function
falls back to sane local-development defaults.

Usage in `main.py`:
    from app.core.middleware import setup_cors
    setup_cors(app)
"""
from typing import List, Optional
import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import config


def _parse_env_origins() -> Optional[List[str]]:
    val = os.getenv("CORS_ALLOWED_ORIGINS") or os.getenv("ALLOWED_ORIGINS")
    if not val:
        return None
    val = val.strip()
    # Accept JSON array or comma separated list
    if val.startswith("["):
        try:
            parsed = json.loads(val)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except Exception:
            pass
    return [p.strip() for p in val.split(",") if p.strip()]


def setup_cors(app: FastAPI) -> None:
    """Attach CORS middleware to `app`.

    Priority for origin list:
      1. `config.cors_allowed_origins` if present
      2. `CORS_ALLOWED_ORIGINS` env var (comma-separated or JSON array)
      3. local development defaults

    For Render: set the `CORS_ALLOWED_ORIGINS` service env var to your
    frontend URL(s) (e.g. https://my-frontend.onrender.com). Avoid ``*``
    in production unless you explicitly need it.
    """

    origins = getattr(config, "cors_allowed_origins", None)
    if not origins:
        origins = _parse_env_origins()

    if not origins:
        origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:3000",
        ]

    # Allow a single '*' entry to mean allow all origins
    allow_all = len(origins) == 1 and origins[0] == "*"

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*" if allow_all else origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
