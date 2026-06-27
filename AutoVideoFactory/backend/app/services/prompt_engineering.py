from __future__ import annotations

from typing import Any, Optional

from ..services.llm_client import get_llm_client
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.prompt")


class PromptEngineeringService:
    def __init__(self) -> None:
        self._llm = get_llm_client()

    async def generate_image_prompt(self, scene_description: str, style: Optional[str] = None) -> str:
        style_hint = f" in {style} style" if style else ""
        prompt = f"""Generate a detailed image generation prompt for this scene description:
'{scene_description}'
Create a prompt suitable for Stable Diffusion / Midjourney{style_hint}.
Focus on visual details, lighting, composition, and mood.
Keep it under 200 words."""
        return await self._llm.generate(prompt, system_prompt="You are an expert prompt engineer for AI image generation.")

    async def generate_video_prompt(self, scene_description: str, duration: float = 5.0) -> str:
        prompt = f"""Generate a video generation prompt for a {duration}-second clip:
Scene: {scene_description}
Include: motion description, camera movement, visual style, mood.
Suitable for text-to-video AI models."""
        return await self._llm.generate(prompt, system_prompt="You are an expert at creating video generation prompts.")

    async def generate_script(self, topic: str, research_data: dict[str, Any], duration_seconds: float = 60.0) -> str:
        word_limit = int(duration_seconds * 2.5)
        prompt = f"""Write a short-form video script about: {topic}

Research context: {research_data.get('summary', '')}
Key points to cover: {research_data.get('key_points', [])}

Requirements:
- Hook in first 3 seconds
- Keep under {word_limit} words
- Target duration: {duration_seconds} seconds
- Clear call to action at end
- Conversational, engaging tone
- Suitable for TikTok/YouTube Shorts/Reels"""
        return await self._llm.generate(prompt, system_prompt="You are a professional short-form video scriptwriter.")

    async def optimize_prompt(self, prompt: str, target_provider: str) -> str:
        prompt_text = f"""Optimize this prompt for {target_provider}:
'{prompt}'
Make it more effective for {target_provider}'s AI model specifically.
Add relevant keywords, improve clarity, ensure best results."""
        return await self._llm.generate(prompt_text, system_prompt="You are an AI prompt optimization expert.")

    async def generate_hashtags(self, topic: str, count: int = 10) -> list[str]:
        prompt = f"""Generate {count} trending hashtags for a video about: {topic}
Mix of broad and niche hashtags. Return as comma-separated list."""
        result = await self._llm.generate(prompt, system_prompt="You are a social media hashtag strategist.")
        return [h.strip().lstrip("#") for h in result.replace("\n", ",").split(",") if h.strip()]

    async def generate_title(self, topic: str, platform: str = "tiktok") -> str:
        prompt = f"""Generate an attention-grabbing title for a {platform} video about: {topic}
Make it curiosity-driven, under 100 characters, optimized for {platform} algorithm."""
        return await self._llm.generate(prompt, system_prompt="You are a viral content title expert.")
