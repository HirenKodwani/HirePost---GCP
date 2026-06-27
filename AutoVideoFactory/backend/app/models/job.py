from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Job(UUIDMixin, TimestampMixin, Base):
    project_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("project.id"), nullable=True
    )
    job_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="pending", index=True
    )
    priority: Mapped[int] = mapped_column(Integer, default=0)
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    progress_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    params_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    is_cancellable: Mapped[bool] = mapped_column(Boolean, default=True)
    pipeline_step: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    agent_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    project = relationship("Project", back_populates="jobs")
    logs = relationship("Log", back_populates="job", cascade="all, delete-orphan")


class Log(UUIDMixin, TimestampMixin, Base):
    job_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("job.id"), nullable=True
    )
    level: Mapped[str] = mapped_column(String(20), default="INFO")
    logger_name: Mapped[str] = mapped_column(String(255), default="root")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    extra_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )

    job = relationship("Job", back_populates="logs")


class Run(UUIDMixin, TimestampMixin, Base):
    pipeline_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="running")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_jobs: Mapped[int] = mapped_column(Integer, default=0)
    completed_jobs: Mapped[int] = mapped_column(Integer, default=0)
    failed_jobs: Mapped[int] = mapped_column(Integer, default=0)
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
