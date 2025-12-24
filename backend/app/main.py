"""FastAPI application entrypoint and startup lifecycle handling.

This module defines the ASGI `lifespan` handler which performs the
one-time startup loading of heavy resources (embeddings, ids, model,
and master dataframe) using the centralized `data_loader` helpers.
Loaded resources are attached to `app.core.config` for process-global
access throughout the application.
"""

from fastapi import FastAPI
from app.api.routes import router
import asyncio

from app.services.data_loader import load_startup_resources
from app.core import config
from app.core.middleware import setup_cors


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


async def _background_init():
    """Run heavy startup loads in a background executor so the app
    can start immediately and respond to health checks.
    """
    loop = asyncio.get_running_loop()
    try:
        embs, ids, model, df = await loop.run_in_executor(None, _init_resources_sync)
        config.embeddings = embs
        config.ids = ids
        config.model = model
        config.df = df
        config.ready = True
        print("background resource initialization completed: ready=True")
    except Exception as e:
        config.embeddings = None
        config.ids = None
        config.model = None
        config.df = None
        config.ready = False
        print(f"Error during background resource initialization: {e}")


app = FastAPI(
    title="Semantic Recipe Finder API",
    description="Search recipes using semantic similarity and get recipe details",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"service": "Semantic Recipe Finder API", "status": "ok", "ready": getattr(config, "ready", False)}

setup_cors(app)
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    # schedule background initialization but don't await it so startup is fast
    asyncio.create_task(_background_init())


@app.get("/ready")
def ready():
    """Simple readiness endpoint used by health checks. Returns 200
    immediately; `ready: true` once heavy resources have finished loading.
    """
    return {"ready": bool(getattr(config, "ready", False))}
