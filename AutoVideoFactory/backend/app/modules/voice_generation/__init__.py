from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class VoiceGenerationResult(BaseModel):
    file_path: str
    duration_seconds: float = 0.0
    text_used: str = ""
    voice_id: str = ""
    provider: str = ""


class VoiceGenerationModuleInterface(ModuleInterface):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="text_to_speech",
                description="Convert text to natural-sounding speech",
                supported_providers=["edge-tts", "elevenlabs", "openai", "coqui"],
            ),
            ModuleCapability(
                name="voice_cloning",
                description="Clone voices from audio samples",
            ),
        ]

    @abstractmethod
    async def generate_speech(self, text: str, voice_id: str, **kwargs) -> VoiceGenerationResult:
        ...

    @abstractmethod
    async def list_voices(self, language: Optional[str] = None) -> list[dict]:
        ...

    @abstractmethod
    async def clone_voice(self, audio_path: str, name: str) -> str:
        ...

    @abstractmethod
    async def generate_with_timing(self, text: str, voice_id: str, word_timings: bool = True) -> VoiceGenerationResult:
        ...
