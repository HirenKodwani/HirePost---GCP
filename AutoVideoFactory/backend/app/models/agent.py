from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin


class AgentState(UUIDMixin, TimestampMixin, Base):
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="idle")
    current_task: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    current_job_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tasks_completed: Mapped[int] = mapped_column(Integer, default=0)
    tasks_failed: Mapped[int] = mapped_column(Integer, default=0)


class AgentMessage(UUIDMixin, TimestampMixin, Base):
    sender: Mapped[str] = mapped_column(String(100), nullable=False)
    receiver: Mapped[str] = mapped_column(String(100), nullable=False)
    message_type: Mapped[str] = mapped_column(String(100), nullable=False)
    content_json: Mapped[str] = mapped_column(Text, nullable=False)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    response_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
