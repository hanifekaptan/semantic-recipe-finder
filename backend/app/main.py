"""FastAPI application entrypoint and startup lifecycle handling.

This module defines the ASGI `lifespan` handler which performs the
one-time startup loading of heavy resources (embeddings, ids, model,
and master dataframe) using the centralized `data_loader` helpers.
Loaded resources are attached to `app.core.config` for process-global
access throughout the application.
"""

from fastapi import FastAPI
from app.api.routes import router
from contextlib import asynccontextmanager
import asyncio

from app.services.data_loader import load_startup_resources
from app.core import config
from app.core.middleware import setup_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ASGI lifespan handler.

    Loads required startup resources in a background executor to avoid
    blocking the event loop. Any resources that fail to load are set to
    `None` and a warning is printed; application continues to run so
    health checks and tests can run in degraded mode.
    """

    loop = asyncio.get_running_loop()

    def _init_resources_sync():
        embs, ids, model, df, err = load_startup_resources(
            config.metadata_embeddings_path,
            config.recipe_ids_path,
            config.model_name,
            config.recipes_details_path,
        )
        if err:
            print(f"startup load warning: {err}")
        return embs, ids, model, df

    try:
        embs, ids, model, df = await loop.run_in_executor(None, _init_resources_sync)
    except Exception as e:
        print(f"Error during startup resource initialization: {e}")
        embs = ids = model = df = None

    config.embeddings = embs
    config.ids = ids
    config.model = model
    config.df = df
    yield


app = FastAPI(
    title="Semantic Recipe Finder API",
    description="Search recipes using semantic similarity and get recipe details",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"service": "Semantic Recipe Finder API", "status": "ok"}

setup_cors(app)
app.include_router(router)
