from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

import urllib.parse

from ..core.config import settings
from ..core.exceptions import ProviderError
from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.image_providers")


class ImageGenerationProvider(ABC):
    provider_name: str = "base"

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        ...

    @abstractmethod
    async def generate_variation(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        ...


class PollinationsProvider(ImageGenerationProvider):
    provider_name = "pollinations"

    async def generate(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        try:
            width = kwargs.get("width", 1024)
            height = kwargs.get("height", 1024)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width={width}&height={height}"
            return {"url": url, "provider": "pollinations", "prompt": prompt}
        except Exception as e:
            raise ProviderError(f"Pollinations failed: {e}") from e

    async def generate_variation(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return await self.generate(prompt, **kwargs)


class StableDiffusionProvider(ImageGenerationProvider):
    provider_name = "stability"

    async def generate(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        width = kwargs.get("width", 1024)
        height = kwargs.get("height", 1024)
        logger.info(f"SD generating: {prompt[:50]}... ({width}x{height})")
        return {"provider": "stability", "prompt": prompt, "status": "mock"}

    async def generate_variation(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return await self.generate(prompt, **kwargs)


class ComfyUIProvider(ImageGenerationProvider):
    provider_name = "comfyui"

    async def generate(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"ComfyUI generating: {prompt[:50]}...")
        return {"provider": "comfyui", "prompt": prompt, "status": "mock"}

    async def generate_variation(self, image_path: str, prompt: str, **kwargs: Any) -> dict[str, Any]:
        return await self.generate(prompt, **kwargs)


class ImageProviderRegistry:
    _providers: dict[str, type[ImageGenerationProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[ImageGenerationProvider]) -> None:
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> ImageGenerationProvider:
        provider_class = cls._providers.get(name)
        if not provider_class:
            raise ProviderError(f"Unknown image provider: {name}", provider_name=name)
        return provider_class()

    @classmethod
    def list_providers(cls) -> list[dict[str, str]]:
        return [{"name": n, "class": p.__name__} for n, p in cls._providers.items()]


ImageProviderRegistry.register("pollinations", PollinationsProvider)
ImageProviderRegistry.register("stability", StableDiffusionProvider)
ImageProviderRegistry.register("comfyui", ComfyUIProvider)
