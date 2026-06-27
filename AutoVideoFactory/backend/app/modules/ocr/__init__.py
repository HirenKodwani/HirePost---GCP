from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

import numpy as np
from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class OCRResult(BaseModel):
    text: str
    confidence: float = 0.0
    regions: list[dict[str, Any]] = []


class OCRModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="text_extraction",
                description="Extract text from images using OCR",
                supported_providers=["tesseract", "easyocr", "paddleocr"],
            ),
            ModuleCapability(
                name="text_search",
                description="Search for specific text in images",
            ),
        ]

    @abstractmethod
    async def extract_text(self, image: np.ndarray, language: str = "eng") -> OCRResult:
        ...

    @abstractmethod
    async def find_text(self, image: np.ndarray, target_text: str) -> Optional[dict[str, Any]]:
        ...

    @abstractmethod
    async def extract_structured(self, image: np.ndarray, schema: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def detect_language(self, image: np.ndarray) -> str:
        ...
