"""FastAPI application entrypoint and startup lifecycle handling.

This module defines the ASGI `lifespan` handler which performs the
one-time startup loading of heavy resources (embeddings, ids, model,
and master dataframe) using the centralized `data_loader` helpers.
Loaded resources are attached to `app.core.config` for process-global
access throughout the application.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import os

from app.api.routes import router
from app.services.loading_service import load_startup_resources
from app.services.detail_service import DetailService
from app.services.search_service import SearchService
from app.core import config
from app.core.logging import configure_logging, get_logger


configure_logging(level=os.getenv("LOG_LEVEL", "INFO"), log_file=os.getenv("LOG_FILE", None))
logger = get_logger(__name__)


def initialize_startup_resources() -> None:
    """Load model, dataframe and chroma collection and attach to `config`.

    Errors are logged and the process continues in degraded mode.
    """
    try:
        model, df, chroma_col, err = load_startup_resources(
            config.metadata_embeddings_path,
            config.recipe_ids_path,
            config.model_name,
            config.recipes_details_path,
        )
        if err:
            logger.warning("startup load warning: %s", err)

        config.model = model
        config.df = df
        config.chroma_collection = chroma_col
        
        logger.info("Resources loaded - model: %s, df: %s (shape: %s), chroma: %s", 
                   model is not None, 
                   df is not None, 
                   df.shape if df is not None else None,
                   chroma_col is not None)

        try:
            config.detail_service = DetailService(df)
            # initialize search service so API can use it without lazy init
            try:
                config.search_service = SearchService(model=model, chroma_collection=chroma_col, df=df)
            except Exception:
                logger.exception("failed creating SearchService")
        except Exception:
            logger.exception("failed creating card/detail services")

        config.ready = True if (model is not None and df is not None) else False
        logger.info("startup complete: ready=%s", config.ready)
    except Exception:
        config.model = None
        config.df = None
        config.chroma_collection = None
        config.ready = False
        logger.exception("unexpected error during startup initialization")


# --- APPLICATION CREATION & ROUTES ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting application startup tasks via lifespan")
    initialize_startup_resources()
    yield


app = FastAPI(title="Semantic Recipe Finder API", version="1.0.0", lifespan=lifespan)


@app.get("/")
def root():
    logger.debug("root endpoint hit; redirecting to /docs")
    return RedirectResponse(url="/docs")

app.include_router(router)
