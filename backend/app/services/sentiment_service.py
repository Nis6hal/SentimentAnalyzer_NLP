"""
Business logic and persistence service for SentimentIQ.
Interfaces the ML Inference Engine with SQLAlchemy DB sessions.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from ml.inference.engine import SentimentInferenceEngine
from backend.app.models.entities import AnalysisRecord, UserFeedback, ModelVersion
from backend.app.schemas.sentiment import (
    SentimentResult, SentimentProbabilities, HistoryItem,
    AnalyticsResponse, SentimentCount, ModelInfoResponse
)
from backend.app.core.config import settings

logger = logging.getLogger("sentimentiq.service")


class SentimentService:
    def __init__(self, engine: Optional[SentimentInferenceEngine] = None):
        if engine:
            self.inference_engine = engine
        else:
            self.inference_engine = SentimentInferenceEngine.get_instance(
                model_type=settings.MODEL_TYPE,
                device=settings.DEVICE
            )

    async def analyze_text(self, db: AsyncSession, text: str, source: str = "single") -> SentimentResult:
        """Runs model inference on a single text and persists the record to the database."""
        raw_res = self.inference_engine.predict(text)
        res_data = raw_res["result"]
        probs = res_data["probabilities"]

        preview = text[:150] + "..." if len(text) > 150 else text

        record = AnalysisRecord(
            text=text,
            text_preview=preview,
            sentiment=res_data["sentiment"],
            confidence=res_data["confidence"],
            positive_prob=probs["positive"],
            negative_prob=probs["negative"],
            neutral_prob=probs["neutral"],
            model_version=res_data["model_version"],
            model_id=res_data["model_id"],
            latency_ms=res_data.get("latency_ms"),
            source=source
        )

        db.add(record)
        await db.commit()
        await db.refresh(record)

        return SentimentResult(
            id=record.id,
            sentiment=record.sentiment,
            confidence=record.confidence,
            probabilities=SentimentProbabilities(
                positive=record.positive_prob,
                negative=record.negative_prob,
                neutral=record.neutral_prob
            ),
            model_version=record.model_version,
            model_id=record.model_id,
            latency_ms=record.latency_ms,
            created_at=record.created_at
        )

    async def analyze_batch(self, db: AsyncSession, texts: List[str]) -> List[SentimentResult]:
        """Runs batched inference across texts and bulk-persists records."""
        raw_results = self.inference_engine.predict_batch(texts)
        results = []
        db_records = []

        for idx, r in enumerate(raw_results):
            res_data = r["result"]
            probs = res_data["probabilities"]
            text = texts[idx]
            preview = text[:150] + "..." if len(text) > 150 else text

            record = AnalysisRecord(
                text=text,
                text_preview=preview,
                sentiment=res_data["sentiment"],
                confidence=res_data["confidence"],
                positive_prob=probs["positive"],
                negative_prob=probs["negative"],
                neutral_prob=probs["neutral"],
                model_version=res_data["model_version"],
                model_id=res_data["model_id"],
                latency_ms=res_data.get("latency_ms"),
                source="batch"
            )
            db_records.append(record)

        db.add_all(db_records)
        await db.commit()

        for rec in db_records:
            await db.refresh(rec)
            results.append(
                SentimentResult(
                    id=rec.id,
                    sentiment=rec.sentiment,
                    confidence=rec.confidence,
                    probabilities=SentimentProbabilities(
                        positive=rec.positive_prob,
                        negative=rec.negative_prob,
                        neutral=rec.neutral_prob
                    ),
                    model_version=rec.model_version,
                    model_id=rec.model_id,
                    latency_ms=rec.latency_ms,
                    created_at=rec.created_at
                )
            )

        return results

    async def get_history(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        sentiment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Queries paginated history records."""
        query = select(AnalysisRecord)
        if sentiment and sentiment.upper() in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
            query = query.where(AnalysisRecord.sentiment == sentiment.upper())

        # Total count
        count_query = select(func.count(AnalysisRecord.id))
        if sentiment and sentiment.upper() in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
            count_query = count_query.where(AnalysisRecord.sentiment == sentiment.upper())
        total_res = await db.execute(count_query)
        total = total_res.scalar_one()

        offset = (page - 1) * page_size
        query = query.order_by(desc(AnalysisRecord.created_at)).offset(offset).limit(page_size)
        records_res = await db.execute(query)
        records = records_res.scalars().all()

        items = []
        for r in records:
            items.append(
                HistoryItem(
                    id=r.id,
                    text=r.text,
                    text_preview=r.text_preview,
                    sentiment=r.sentiment,
                    confidence=r.confidence,
                    probabilities=SentimentProbabilities(
                        positive=r.positive_prob,
                        negative=r.negative_prob,
                        neutral=r.neutral_prob
                    ),
                    model_id=r.model_id,
                    model_version=r.model_version,
                    source=r.source,
                    latency_ms=r.latency_ms,
                    created_at=r.created_at
                )
            )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }

    async def get_analytics(self, db: AsyncSession) -> AnalyticsResponse:
        """Computes aggregate distribution, sentiment percentages, latency, and trends."""
        # Total counts by sentiment
        sentiment_stmt = select(
            AnalysisRecord.sentiment,
            func.count(AnalysisRecord.id)
        ).group_by(AnalysisRecord.sentiment)
        
        counts_res = await db.execute(sentiment_stmt)
        sentiment_counts = {row[0]: row[1] for row in counts_res.all()}

        pos_count = sentiment_counts.get("POSITIVE", 0)
        neg_count = sentiment_counts.get("NEGATIVE", 0)
        neu_count = sentiment_counts.get("NEUTRAL", 0)
        total_count = pos_count + neg_count + neu_count

        percentages = {
            "positive": round((pos_count / total_count * 100.0) if total_count > 0 else 0.0, 1),
            "negative": round((neg_count / total_count * 100.0) if total_count > 0 else 0.0, 1),
            "neutral": round((neu_count / total_count * 100.0) if total_count > 0 else 0.0, 1)
        }

        # Averages
        avg_stmt = select(
            func.avg(AnalysisRecord.confidence),
            func.avg(AnalysisRecord.latency_ms)
        )
        avg_res = await db.execute(avg_stmt)
        avg_conf, avg_lat = avg_res.one()

        # Recent 10 items for quick feed
        recent_res = await db.execute(
            select(AnalysisRecord).order_by(desc(AnalysisRecord.created_at)).limit(10)
        )
        recent_records = recent_res.scalars().all()
        recent_items = [
            HistoryItem(
                id=r.id,
                text=r.text,
                text_preview=r.text_preview,
                sentiment=r.sentiment,
                confidence=r.confidence,
                probabilities=SentimentProbabilities(
                    positive=r.positive_prob,
                    negative=r.negative_prob,
                    neutral=r.neutral_prob
                ),
                model_id=r.model_id,
                model_version=r.model_version,
                source=r.source,
                latency_ms=r.latency_ms,
                created_at=r.created_at
            ) for r in recent_records
        ]

        # Timeline aggregate (grouped by date)
        timeline_stmt = select(
            func.date(AnalysisRecord.created_at).label("date_label"),
            AnalysisRecord.sentiment,
            func.count(AnalysisRecord.id)
        ).group_by("date_label", AnalysisRecord.sentiment).order_by("date_label")

        timeline_res = await db.execute(timeline_stmt)
        timeline_map = {}
        for row in timeline_res.all():
            d_str = str(row[0])
            s = row[1]
            cnt = row[2]
            if d_str not in timeline_map:
                timeline_map[d_str] = {"date": d_str, "positive": 0, "negative": 0, "neutral": 0, "total": 0}
            timeline_map[d_str][s.lower()] += cnt
            timeline_map[d_str]["total"] += cnt

        timeline = list(timeline_map.values())

        return AnalyticsResponse(
            success=True,
            summary=SentimentCount(
                positive=pos_count,
                negative=neg_count,
                neutral=neu_count,
                total=total_count
            ),
            percentages=percentages,
            average_confidence=round(float(avg_conf or 0.0), 4),
            average_latency_ms=round(float(avg_lat or 0.0), 2),
            timeline=timeline,
            recent_activity=recent_items
        )

    async def submit_feedback(
        self,
        db: AsyncSession,
        analysis_id: int,
        is_correct: bool,
        actual_sentiment: Optional[str] = None,
        comment: Optional[str] = None
    ) -> bool:
        """Stores user correction or rating for model predictions."""
        # Check record exists
        rec = await db.get(AnalysisRecord, analysis_id)
        if not rec:
            return False

        feedback = UserFeedback(
            analysis_id=analysis_id,
            is_correct=is_correct,
            actual_sentiment=actual_sentiment,
            comment=comment
        )
        db.add(feedback)
        await db.commit()
        return True

    def get_model_info(self) -> ModelInfoResponse:
        """Returns active model details and empirical benchmark figures."""
        info = self.inference_engine.get_model_info()
        benchmark_data = {
            "test_macro_f1": 0.7043 if info["model_type"] == "champion" else 0.5837,
            "test_accuracy": 0.6990 if info["model_type"] == "champion" else 0.5868,
            "challenge_suite_accuracy": 0.7500 if info["model_type"] == "champion" else 0.3750,
            "f1_negative": 0.7009 if info["model_type"] == "champion" else 0.5998,
            "f1_neutral": 0.6861 if info["model_type"] == "champion" else 0.5860,
            "f1_positive": 0.7259 if info["model_type"] == "champion" else 0.5655
        }

        desc = (
            "CardiffNLP RoBERTa Fine-Tuned Sentiment Model evaluated on TweetEval and SST-2."
            if info["model_type"] == "champion" else
            "TF-IDF (1-3 ngrams) with Scikit-learn Balanced Logistic Regression Baseline."
        )

        return ModelInfoResponse(
            success=True,
            model_id=info["model_id"],
            model_type=info["model_type"],
            version=info["version"],
            classes=info["classes"],
            device=info["device"],
            is_loaded=info["is_loaded"],
            benchmark=benchmark_data,
            description=desc
        )

