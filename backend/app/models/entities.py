"""
SQLAlchemy Entity Models for SentimentIQ.
Entities for Analysis Records, Probabilities, Feedback, Users, and Model Versions.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from backend.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    analyses = relationship("AnalysisRecord", back_populates="user", cascade="all, delete-orphan")


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    text = Column(Text, nullable=False)
    text_preview = Column(String(200), nullable=False)
    sentiment = Column(String(20), nullable=False, index=True)  # POSITIVE, NEGATIVE, NEUTRAL
    confidence = Column(Float, nullable=False)

    # Individual class probabilities
    negative_prob = Column(Float, nullable=False)
    neutral_prob = Column(Float, nullable=False)
    positive_prob = Column(Float, nullable=False)

    model_version = Column(String(50), nullable=False, default="1.0.0")
    model_id = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=True)
    source = Column(String(20), default="single")  # "single" or "batch"
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", back_populates="analyses")
    feedback = relationship("UserFeedback", back_populates="analysis", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_sentiment_created", "sentiment", "created_at"),
    )


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_records.id", ondelete="CASCADE"), nullable=False, unique=True)
    is_correct = Column(Boolean, nullable=False)
    actual_sentiment = Column(String(20), nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    analysis = relationship("AnalysisRecord", back_populates="feedback")


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    architecture = Column(String(100), nullable=False)
    macro_f1 = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

