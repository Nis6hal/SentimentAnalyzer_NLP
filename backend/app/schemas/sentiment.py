"""
Pydantic Request & Response Schemas for SentimentIQ.
"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class SentimentProbabilities(BaseModel):
    positive: float = Field(..., ge=0.0, le=1.0)
    negative: float = Field(..., ge=0.0, le=1.0)
    neutral: float = Field(..., ge=0.0, le=1.0)


class SentimentResult(BaseModel):
    sentiment: str = Field(..., description="POSITIVE, NEGATIVE, or NEUTRAL")
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: SentimentProbabilities
    model_version: str
    model_id: str
    latency_ms: Optional[float] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000, description="Raw English text to analyze")


class AnalyzeResponse(BaseModel):
    success: bool = True
    result: SentimentResult


class BatchAnalyzeRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=500, description="List of texts to analyze in a batch")


class BatchAnalyzeResponse(BaseModel):
    success: bool = True
    results: List[SentimentResult]
    total_processed: int
    average_latency_ms: float


class HistoryItem(BaseModel):
    id: int
    text: str
    text_preview: str
    sentiment: str
    confidence: float
    probabilities: SentimentProbabilities
    model_id: str
    model_version: str
    source: str
    latency_ms: Optional[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoryResponse(BaseModel):
    success: bool = True
    total: int
    page: int
    page_size: int
    items: List[HistoryItem]


class SentimentCount(BaseModel):
    positive: int = 0
    negative: int = 0
    neutral: int = 0
    total: int = 0


class AnalyticsResponse(BaseModel):
    success: bool = True
    summary: SentimentCount
    percentages: Dict[str, float]
    average_confidence: float
    average_latency_ms: float
    timeline: List[Dict[str, str | int]]
    recent_activity: List[HistoryItem]


class ModelInfoResponse(BaseModel):
    success: bool = True
    model_id: str
    model_type: str
    version: str
    classes: List[str]
    device: str
    is_loaded: bool
    benchmark: Dict[str, float]
    description: str


class FeedbackRequest(BaseModel):
    analysis_id: int
    is_correct: bool
    actual_sentiment: Optional[str] = None
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    success: bool = True
    message: str
