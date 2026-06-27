from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Project(UUIDMixin, TimestampMixin, Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    niche: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_platform: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_audience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_count: Mapped[int] = mapped_column(Integer, default=0)
    total_duration: Mapped[float] = mapped_column(Float, default=0.0)
    scheduled_publish_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    topics = relationship("Topic", back_populates="project", cascade="all, delete-orphan")
    scripts = relationship("Script", back_populates="project", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="project", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="project", cascade="all, delete-orphan")


class Topic(UUIDMixin, TimestampMixin, Base):
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("project.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trend_score: Mapped[float] = mapped_column(Float, default=0.0)
    search_volume: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    competition_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    project = relationship("Project", back_populates="topics")
    scripts = relationship("Script", back_populates="topic")


class Script(UUIDMixin, TimestampMixin, Base):
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("project.id"), nullable=False
    )
    topic_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("topic.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    estimated_duration: Mapped[float] = mapped_column(Float, default=0.0)
    tone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    is_optimized: Mapped[bool] = mapped_column(Boolean, default=False)
    prompt_used: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    project = relationship("Project", back_populates="scripts")
    topic = relationship("Topic", back_populates="scripts")
    scenes = relationship("Scene", back_populates="script", cascade="all, delete-orphan")
    prompts = relationship("Prompt", back_populates="script", cascade="all, delete-orphan")


class Scene(UUIDMixin, TimestampMixin, Base):
    script_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("script.id"), nullable=False
    )
    scene_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    visual_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[float] = mapped_column(Float, default=5.0)
    transition_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    script = relationship("Script", back_populates="scenes")
    prompts = relationship("Prompt", back_populates="scene", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="scene", cascade="all, delete-orphan")
