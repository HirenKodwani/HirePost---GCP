from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Optional

import httpx

from ..core.exceptions import ContentGenerationError
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.voice")


class VoiceService:
    MOOD_VOICE_MAP: dict[str, dict[str, str]] = {
        "energetic": {"voice": "en-US-JennyNeural", "rate": "+30%", "pitch": "+15Hz"},
        "educational": {"voice": "en-US-GuyNeural", "rate": "+0%", "pitch": "+0Hz"},
        "dramatic": {"voice": "en-US-AriaNeural", "rate": "-10%", "pitch": "-5Hz"},
        "humorous": {"voice": "en-US-JennyNeural", "rate": "+20%", "pitch": "+10Hz"},
        "serious": {"voice": "en-US-GuyNeural", "rate": "+10%", "pitch": "-10Hz"},
    }

    def __init__(self) -> None:
        self._output_dir = Path("output/voice")
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_edge_tts(self, text: str, voice: str = "en-US-JennyNeural", rate: str = "+0%", pitch: str = "+0Hz") -> dict[str, Any]:
        output_path = self._output_dir / f"voice_{abs(hash(text))}.mp3"
        duration = len(text.split()) * 0.35
        for attempt in range(3):
            try:
                import edge_tts
                communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                await communicate.save(str(output_path))
                return {"file_path": str(output_path), "duration_seconds": duration, "voice": voice, "provider": "edge-tts"}
            except ImportError:
                logger.warning("edge-tts not installed")
                break
            except Exception as e:
                logger.warning(f"Edge TTS attempt {attempt+1}/3 failed: {e}")
                if attempt == 2:
                    break
                await asyncio.sleep(3)
        logger.warning("edge-tts failed, generating silent audio")
        try:
            import subprocess
            cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono", "-t", str(max(duration, 5)), "-c:a", "aac", "-b:a", "64k", str(output_path)]
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
        except Exception:
            output_path.write_bytes(b"")
        return {"file_path": str(output_path), "duration_seconds": duration, "voice": voice, "provider": "fallback"}

    async def generate_with_mood(self, text: str, mood: str = "educational") -> dict[str, Any]:
        config = self.MOOD_VOICE_MAP.get(mood, self.MOOD_VOICE_MAP["educational"])
        return await self.generate_edge_tts(text, voice=config["voice"], rate=config["rate"], pitch=config["pitch"])

    async def generate_elevenlabs(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", api_key: str = "") -> dict[str, Any]:
        try:
            if not api_key:
                return await self.generate_edge_tts(text)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                    json={"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}},
                )
                response.raise_for_status()
                output_path = self._output_dir / f"eleven_{abs(hash(text))}.mp3"
                output_path.write_bytes(response.content)
                return {"file_path": str(output_path), "duration_seconds": len(text.split()) * 0.35, "voice_id": voice_id, "provider": "elevenlabs"}
        except Exception as e:
            raise ContentGenerationError(f"ElevenLabs TTS failed: {e}") from e

    async def list_voices(self) -> list[dict[str, str]]:
        return [
            {"id": "en-US-JennyNeural", "name": "Jenny", "gender": "Female", "language": "en", "provider": "edge-tts"},
            {"id": "en-US-GuyNeural", "name": "Guy", "gender": "Male", "language": "en", "provider": "edge-tts"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia", "gender": "Female", "language": "en", "provider": "edge-tts"},
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "gender": "Female", "language": "en", "provider": "elevenlabs"},
        ]

    async def generate_with_timing(self, text: str, voice_id: str = "en-US-JennyNeural") -> dict[str, Any]:
        result = await self.generate_edge_tts(text, voice_id)
        words = text.split()
        avg_word_duration = result["duration_seconds"] / max(len(words), 1)
        result["segments"] = [
            {"word": w, "start": i * avg_word_duration, "end": (i + 1) * avg_word_duration}
            for i, w in enumerate(words)
        ]
        return result
