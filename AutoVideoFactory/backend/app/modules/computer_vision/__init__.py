from __future__ import annotations

from abc import abstractmethod
from typing import Any, Optional

import numpy as np
from pydantic import BaseModel

from ..base import ModuleCapability, ModuleInterface


class DetectedRegion(BaseModel):
    x: int
    y: int
    width: int
    height: int
    label: str = ""
    confidence: float = 0.0


class LoadingState(BaseModel):
    is_loading: bool = False
    progress: float = 0.0
    detected_by: str = ""


class ComputerVisionModuleInterface(ModuleInterface[Any]):
    def get_capabilities(self):
        return [
            ModuleCapability(
                name="template_matching",
                description="Match visual templates in screenshots",
            ),
            ModuleCapability(
                name="loading_detection",
                description="Detect loading states from screenshots",
            ),
            ModuleCapability(
                name="element_detection",
                description="Detect UI elements visually",
            ),
        ]

    @abstractmethod
    async def find_template(
        self, screenshot: np.ndarray, template: np.ndarray, threshold: float = 0.8
    ) -> Optional[DetectedRegion]:
        ...

    @abstractmethod
    async def detect_loading(self, screenshot: np.ndarray) -> LoadingState:
        ...

    @abstractmethod
    async def find_text_region(
        self, screenshot: np.ndarray, text: str
    ) -> Optional[DetectedRegion]:
        ...

    @abstractmethod
    async def detect_button(self, screenshot: np.ndarray, label: str) -> Optional[DetectedRegion]:
        ...

    @abstractmethod
    async def compare_images(
        self, img1: np.ndarray, img2: np.ndarray
    ) -> float:
        ...

    @abstractmethod
    async def preprocess(self, image: np.ndarray) -> np.ndarray:
        ...
