from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class VideoMetadata(BaseModel):
    title: str = ""
    description: str = ""
    tags: list[str] = []
    category: str = ""
    language: str = "en"
    is_made_for_kids: bool = False
    allow_embedding: bool = True
    allow_comments: bool = True
    visibility: str = "public"
    platform_specific: dict[str, Any] = {}


class MetadataGeneratorModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="metadata_generation",
                description="Generate complete video metadata for publishing",
            ),
        ]

    @abstractmethod
    async def generate(self, title: str, script: str, platform: str = "youtube") -> VideoMetadata:
        ...

    @abstractmethod
    async def format_for_platform(self, metadata: VideoMetadata, platform: str) -> dict:
        ...

    @abstractmethod
    async def validate(self, metadata: VideoMetadata, platform: str) -> list[str]:
        ...
