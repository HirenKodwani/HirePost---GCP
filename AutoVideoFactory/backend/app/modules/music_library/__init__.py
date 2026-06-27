from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class MusicTrack(BaseModel):
    title: str
    artist: str = ""
    file_path: str = ""
    duration_seconds: float = 0.0
    genre: str = ""
    mood: str = ""
    tempo: int = 120
    is_royalty_free: bool = True
    source: str = "local"


class MusicLibraryModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="music_management",
                description="Manage local music library for video backgrounds",
            ),
            ModuleCapability(
                name="music_recommendation",
                description="Recommend music based on video mood and pacing",
            ),
        ]

    @abstractmethod
    async def search(self, query: str, mood: Optional[str] = None, genre: Optional[str] = None) -> list[MusicTrack]:
        ...

    @abstractmethod
    async def get_recommendations(self, mood: str, duration: float, tempo: Optional[int] = None) -> list[MusicTrack]:
        ...

    @abstractmethod
    async def add_track(self, file_path: str, metadata: Optional[dict] = None) -> MusicTrack:
        ...

    @abstractmethod
    async def analyze_track(self, file_path: str) -> dict:
        ...
