from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class AnalyticsEvent(UUIDMixin, TimestampMixin, Base):
    event_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    video_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("video.id"), nullable=True
    )
    job_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("job.id"), nullable=True
    )
    data_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, index=True
    )


class Metric(UUIDMixin, TimestampMixin, Base):
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    metric_value: Mapped[float] = mapped_column(Float, default=0.0)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tags_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )


class QualityScore(UUIDMixin, TimestampMixin, Base):
    video_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("video.id"), nullable=True
    )
    prompt_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("prompt.id"), nullable=True
    )
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    visual_score: Mapped[float] = mapped_column(Float, default=0.0)
    audio_score: Mapped[float] = mapped_column(Float, default=0.0)
    content_score: Mapped[float] = mapped_column(Float, default=0.0)
    engagement_prediction: Mapped[float] = mapped_column(Float, default=0.0)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_approved: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)


class PromptHistory(UUIDMixin, TimestampMixin, Base):
    prompt_type: Mapped[str] = mapped_column(String(50), nullable=False)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    optimized_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    generation_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    params_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class LearningData(UUIDMixin, TimestampMixin, Base):
    data_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    input_json: Mapped[str] = mapped_column(Text, nullable=False)
    output_json: Mapped[str] = mapped_column(Text, nullable=False)
    feedback_score: Mapped[float] = mapped_column(Float, default=0.0)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    source_agent: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
