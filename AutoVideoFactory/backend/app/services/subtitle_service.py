from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

from ..core.exceptions import ContentGenerationError
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.subtitle")


class SubtitleService:
    def __init__(self) -> None:
        self._output_dir = Path("output/subtitles")
        self._output_dir.mkdir(parents=True, exist_ok=True)

    async def transcribe(self, audio_path: str, language: str = "en") -> dict[str, Any]:
        if not os.path.exists(audio_path):
            raise ContentGenerationError(f"Audio not found: {audio_path}")

        try:
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, language=language)
            output_path = self._output_dir / f"{Path(audio_path).stem}.srt"
            self._write_srt(result["segments"], str(output_path))
            return {
                "file_path": str(output_path),
                "segments": result["segments"],
                "language": language,
                "provider": "whisper",
            }
        except ImportError:
            logger.warning("whisper not installed, generating mock subtitles")
            segments = await self._generate_mock_segments(audio_path)
            output_path = self._output_dir / f"{Path(audio_path).stem}.srt"
            self._write_srt(segments, str(output_path))
            return {
                "file_path": str(output_path),
                "segments": segments,
                "language": language,
                "provider": "mock",
            }
        except Exception as e:
            raise ContentGenerationError(f"Transcription failed: {e}") from e

    async def generate_from_text(self, text: str, word_timings: Optional[list[dict]] = None) -> dict[str, Any]:
        if word_timings:
            segments = [
                {"start": w["start"], "end": w["end"], "text": w["word"]}
                for w in word_timings
            ]
        else:
            words = text.split()
            duration_per_word = 0.35
            segments = [
                {"start": i * duration_per_word, "end": (i + 1) * duration_per_word, "text": word}
                for i, word in enumerate(words)
            ]

        output_path = self._output_dir / f"subtitle_{abs(hash(text))}.srt"
        self._write_srt(segments, str(output_path))
        return {"file_path": str(output_path), "segments": segments, "format": "srt"}

    async def translate(self, subtitle_path: str, target_language: str) -> dict[str, Any]:
        if not os.path.exists(subtitle_path):
            raise ContentGenerationError(f"Subtitle not found: {subtitle_path}")
        output_path = subtitle_path.replace(".srt", f"_{target_language}.srt")
        Path(output_path).write_text(Path(subtitle_path).read_text())
        return {"file_path": output_path, "language": target_language}

    def format_srt(self, segments: list[dict]) -> str:
        lines = []
        for i, seg in enumerate(segments, 1):
            start = self._format_time(seg["start"])
            end = self._format_time(seg["end"])
            text = seg.get("text", "")
            lines.append(f"{i}\n{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    def _write_srt(self, segments: list[dict], output_path: str) -> None:
        content = self.format_srt(segments)
        Path(output_path).write_text(content, encoding="utf-8")

    def _format_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    async def _generate_mock_segments(self, audio_path: str) -> list[dict]:
        text = Path(audio_path).stem.replace("_", " ").replace("voice", "").strip()
        if not text:
            text = "This is a sample transcription for the video content."
        words = text.split()
        return [
            {"start": i * 0.35, "end": (i + 1) * 0.35, "text": word}
            for i, word in enumerate(words)
        ]
