"""
SentimentIQ - FastAPI Production Backend Application.
"""

import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.db.session import init_db
from backend.app.api.v1.api import api_router
from ml.inference.engine import SentimentInferenceEngine

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("sentimentiq.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes database tables and pre-warms the ML model into memory.
    """
    logger.info("Initializing SentimentIQ database schema...")
    await init_db()

    logger.info("Pre-warming SentimentIQ ML Inference Engine...")
    engine = SentimentInferenceEngine.get_instance(
        model_type=settings.MODEL_TYPE,
        device=settings.DEVICE
    )
    logger.info(f"ML Model pre-warmed successfully: {engine.model_id}")

    yield

    logger.info("Shutting down SentimentIQ API service...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-grade NLP Sentiment Intelligence API powered by Fine-Tuned Transformer Models.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """Logs incoming request method, path, status, and latency."""
    t0 = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} ({duration_ms}ms)")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global JSON error response formatter."""
    logger.error(f"Unhandled error processing {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "InternalServerError",
            "message": str(exc),
            "path": request.url.path
        }
    )


# Mount versioned API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root_status():
    """Service status overview."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "documentation": "/docs",
        "api_v1": settings.API_V1_STR
    }

