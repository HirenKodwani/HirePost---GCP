from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    niche: Optional[str] = None
    target_platform: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    niche: Optional[str] = None
    target_platform: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    niche: Optional[str] = None
    target_platform: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TopicCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    trend_score: float = 0.0
    keywords: list[str] = []


class ScriptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    tone: Optional[str] = "neutral"
    language: str = "en"


class ScriptResponse(BaseModel):
    id: str
    title: str
    content: str
    word_count: int
    estimated_duration: float
    tone: Optional[str] = None
    created_at: datetime
