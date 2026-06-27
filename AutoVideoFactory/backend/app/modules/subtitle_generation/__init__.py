from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class SubtitleResult(BaseModel):
    content: str
    format_type: str = "srt"
    file_path: str = ""
    language: str = "en"
    segments: list[dict] = []


class SubtitleGenerationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="speech_to_text",
                description="Transcribe speech to text for subtitles",
                supported_providers=["whisper", "deepgram"],
            ),
            ModuleCapability(
                name="subtitle_formatting",
                description="Generate subtitles in various formats (SRT, VTT, ASS)",
            ),
        ]

    @abstractmethod
    async def transcribe(self, audio_path: str, language: str = "en") -> SubtitleResult:
        ...

    @abstractmethod
    async def generate_from_text(self, text: str, word_timings: Optional[list[dict]] = None) -> SubtitleResult:
        ...

    @abstractmethod
    async def translate(self, subtitle_path: str, target_language: str) -> SubtitleResult:
        ...

    @abstractmethod
    async def format_subtitles(self, segments: list[dict], format_type: str = "srt") -> str:
        ...
