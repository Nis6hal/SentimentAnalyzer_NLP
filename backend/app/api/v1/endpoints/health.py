"""
Health Check Endpoint for SentimentIQ.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.db.session import get_db
from ml.inference.engine import SentimentInferenceEngine

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Verifies service health, database connectivity, and ML engine readiness.
    """
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    engine = SentimentInferenceEngine.get_instance()
    engine_status = "loaded" if engine.is_loaded else "not_loaded"

    overall_healthy = (db_status == "healthy") and engine.is_loaded

    return {
        "status": "healthy" if overall_healthy else "degraded",
        "database": db_status,
        "inference_engine": engine_status,
        "model_id": engine.model_id,
        "version": "1.0.0"
    }

