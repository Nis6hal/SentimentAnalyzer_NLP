"""
Main API Router combining version 1 endpoints.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, sentiment

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sentiment.router, tags=["Sentiment Analysis"])

