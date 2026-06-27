from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class CompositionPlan(BaseModel):
    clips: list[dict] = []
    transitions: list[dict] = []
    background_music: Optional[str] = None
    voiceover_path: Optional[str] = None
    subtitle_path: Optional[str] = None
    brand_overlay_path: Optional[str] = None
    output_width: int = 1080
    output_height: int = 1920
    fps: float = 30.0


class VideoEditingModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="video_composition",
                description="Compose final video from clips, audio, and overlays",
                supported_providers=["ffmpeg", "moviepy"],
            ),
            ModuleCapability(
                name="video_effects",
                description="Apply visual effects, transitions, and filters",
            ),
        ]

    @abstractmethod
    async def compose(self, plan: CompositionPlan, output_path: str) -> str:
        ...

    @abstractmethod
    async def add_subtitles(self, video_path: str, subtitle_path: str, burn_in: bool = True) -> str:
        ...

    @abstractmethod
    async def add_background_music(self, video_path: str, music_path: str, volume: float = 0.3) -> str:
        ...

    @abstractmethod
    async def add_brand_overlay(self, video_path: str, overlay_path: str, position: str = "bottom-right") -> str:
        ...

    @abstractmethod
    async def trim(self, video_path: str, start: float, end: float) -> str:
        ...

    @abstractmethod
    async def concatenate(self, video_paths: list[str], transition: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def resize(self, video_path: str, width: int, height: int) -> str:
        ...

    @abstractmethod
    async def add_voiceover(self, video_path: str, audio_path: str) -> str:
        ...
