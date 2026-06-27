from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    job_type: str
    project_id: Optional[str] = None
    priority: int = 0
    params: dict[str, Any] = {}
    max_retries: int = 3


class JobResponse(BaseModel):
    id: str
    job_type: str
    status: str
    progress: float
    progress_message: Optional[str] = None
    priority: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int
    error: Optional[str] = None


class PipelineCreate(BaseModel):
    name: str
    steps: list[dict[str, Any]] = Field(..., min_length=1)
    params: Optional[dict[str, Any]] = None


class PipelineResponse(BaseModel):
    id: str
    name: str
    status: str
    current_step: int
    total_steps: int
    errors: list[str] = []
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
