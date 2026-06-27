from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class ReviewQueueItem(BaseModel):
    video_id: str = ""
    title: str = ""
    status: str = "pending"
    assigned_to: Optional[str] = None
    notes: str = ""
    score: float = 0.0


class HumanReviewModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="review_queue",
                description="Manage human review queue for generated content",
            ),
        ]

    @abstractmethod
    async def add_to_queue(self, video_id: str, priority: int = 0) -> str:
        ...

    @abstractmethod
    async def get_next(self, reviewer_id: Optional[str] = None) -> Optional[ReviewQueueItem]:
        ...

    @abstractmethod
    async def approve(self, review_id: str, notes: Optional[str] = None) -> bool:
        ...

    @abstractmethod
    async def reject(self, review_id: str, reason: str) -> bool:
        ...

    @abstractmethod
    async def list_queue(self, status: Optional[str] = None) -> list[ReviewQueueItem]:
        ...
