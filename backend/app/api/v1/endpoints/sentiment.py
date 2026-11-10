"""
Core Sentiment Analysis Endpoints.
Covers single analysis, batch processing, history, analytics, feedback, and model info.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.sentiment import (
    AnalyzeRequest, AnalyzeResponse,
    BatchAnalyzeRequest, BatchAnalyzeResponse,
    HistoryResponse, AnalyticsResponse,
    ModelInfoResponse, FeedbackRequest, FeedbackResponse
)
from backend.app.services.sentiment_service import SentimentService

router = APIRouter()

# Instantiate single service instance
service = SentimentService()


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_sentiment(
    payload: AnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyzes raw English text, classifies sentiment into POSITIVE, NEGATIVE, or NEUTRAL,
    computes confidence score and class probability distribution, and logs analysis history.
    """
    try:
        result = await service.analyze_text(db=db, text=payload.text, source="single")
        return AnalyzeResponse(success=True, result=result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {str(e)}")


@router.post("/analyze/batch", response_model=BatchAnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_batch_sentiment(
    payload: BatchAnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Performs high-throughput batched sentiment analysis across a list of sentences.
    """
    if not payload.texts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Batch list cannot be empty.")
    
    if len(payload.texts) > 500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Batch exceeds maximum limit of 500 texts.")

    try:
        results = await service.analyze_batch(db=db, texts=payload.texts)
        total = len(results)
        latencies = [r.latency_ms for r in results if r.latency_ms is not None]
        avg_lat = round(sum(latencies) / len(latencies), 2) if latencies else 0.0

        return BatchAnalyzeResponse(
            success=True,
            results=results,
            total_processed=total,
            average_latency_ms=avg_lat
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Batch processing error: {str(e)}")


@router.get("/history", response_model=HistoryResponse, status_code=status.HTTP_200_OK)
async def get_analysis_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment (POSITIVE, NEGATIVE, NEUTRAL)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves paginated history of sentiment classifications with confidence distributions.
    """
    data = await service.get_history(db=db, page=page, page_size=page_size, sentiment=sentiment)
    return HistoryResponse(
        success=True,
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        items=data["items"]
    )


@router.get("/analytics", response_model=AnalyticsResponse, status_code=status.HTTP_200_OK)
async def get_analytics_metrics(db: AsyncSession = Depends(get_db)):
    """
    Returns aggregate sentiment intelligence metrics, class distribution,
    historical trends, and recent analysis feeds.
    """
    return await service.get_analytics(db=db)


@router.get("/model/info", response_model=ModelInfoResponse, status_code=status.HTTP_200_OK)
async def get_model_information():
    """
    Provides architecture details, active weights, and empirical test set benchmarks
    (Macro F1, Accuracy, Challenge Suite Breakdown).
    """
    return service.get_model_info()


@router.post("/feedback", response_model=FeedbackResponse, status_code=status.HTTP_200_OK)
async def submit_prediction_feedback(
    payload: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Records end-user feedback or ground-truth corrections for an analysis record.
    """
    success = await service.submit_feedback(
        db=db,
        analysis_id=payload.analysis_id,
        is_correct=payload.is_correct,
        actual_sentiment=payload.actual_sentiment,
        comment=payload.comment
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis record not found.")

    return FeedbackResponse(success=True, message="Feedback submitted successfully.")

