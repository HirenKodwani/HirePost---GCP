from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..core.config import settings
from ..core.exceptions import ProviderError
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.video_providers")


class VideoGenerationProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        ...

    @abstractmethod
    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_progress(self, task_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_result(self, task_id: str) -> dict[str, Any]:
        ...


class KlingProvider(VideoGenerationProvider):
    provider_name = "kling"

    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Kling generating from prompt: {prompt[:50]}...")
        return {"task_id": "kling_mock", "status": "submitted", "provider": "kling"}

    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Kling generating from image: {image_path}")
        return {"task_id": "kling_img_mock", "status": "submitted", "provider": "kling"}

    async def get_progress(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "progress": 50, "status": "processing"}

    async def get_result(self, task_id: str) -> dict[str, Any]:
        return {
            "task_id": task_id,
            "status": "completed",
            "video_url": f"/output/videos/{task_id}.mp4",
            "duration": 5.0,
        }


class HailuoProvider(VideoGenerationProvider):
    provider_name = "hailuo"

    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Hailuo generating from prompt: {prompt[:50]}...")
        return {"task_id": "hailuo_mock", "status": "submitted", "provider": "hailuo"}

    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return {"task_id": "hailuo_img_mock", "status": "submitted", "provider": "hailuo"}

    async def get_progress(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "progress": 50, "status": "processing"}

    async def get_result(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "status": "completed", "video_url": f"/output/videos/{task_id}.mp4", "duration": 5.0}


class RunwayProvider(VideoGenerationProvider):
    provider_name = "runway"

    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Runway generating from prompt: {prompt[:50]}...")
        return {"task_id": "runway_mock", "status": "submitted", "provider": "runway"}

    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return {"task_id": "runway_img_mock", "status": "submitted", "provider": "runway"}

    async def get_progress(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "progress": 50, "status": "processing"}

    async def get_result(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "status": "completed", "video_url": f"/output/videos/{task_id}.mp4", "duration": 5.0}


class LumaProvider(VideoGenerationProvider):
    provider_name = "luma"

    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Luma generating from prompt: {prompt[:50]}...")
        return {"task_id": "luma_mock", "status": "submitted", "provider": "luma"}

    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return {"task_id": "luma_img_mock", "status": "submitted", "provider": "luma"}

    async def get_progress(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "progress": 50, "status": "processing"}

    async def get_result(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "status": "completed", "video_url": f"/output/videos/{task_id}.mp4", "duration": 5.0}


class WanProvider(VideoGenerationProvider):
    provider_name = "wan"

    async def generate_from_prompt(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"Wan generating from prompt: {prompt[:50]}...")
        return {"task_id": "wan_mock", "status": "submitted", "provider": "wan"}

    async def generate_from_image(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return {"task_id": "wan_img_mock", "status": "submitted", "provider": "wan"}

    async def get_progress(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "progress": 50, "status": "processing"}

    async def get_result(self, task_id: str) -> dict[str, Any]:
        return {"task_id": task_id, "status": "completed", "video_url": f"/output/videos/{task_id}.mp4", "duration": 5.0}


class ProviderRegistry:
    _providers: dict[str, type[VideoGenerationProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[VideoGenerationProvider]) -> None:
        cls._providers[name] = provider_class
        logger.info(f"Registered provider: {name}")

    @classmethod
    def get(cls, name: str) -> VideoGenerationProvider:
        provider_class = cls._providers.get(name)
        if not provider_class:
            raise ProviderError(f"Unknown provider: {name}", provider_name=name)
        return provider_class()

    @classmethod
    def list_providers(cls) -> list[dict[str, str]]:
        return [{"name": name, "class": p.__name__} for name, p in cls._providers.items()]


ProviderRegistry.register("kling", KlingProvider)
ProviderRegistry.register("hailuo", HailuoProvider)
ProviderRegistry.register("runway", RunwayProvider)
ProviderRegistry.register("luma", LumaProvider)
ProviderRegistry.register("wan", WanProvider)
