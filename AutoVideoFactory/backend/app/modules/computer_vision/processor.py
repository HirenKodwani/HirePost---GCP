from __future__ import annotations

from typing import Any, Optional

import cv2
import numpy as np

from ...core.exceptions import OCRVisionError
from ...core.logging import get_logger
from ..base import ModuleHealth, ModuleStatus
from . import ComputerVisionModuleInterface, DetectedRegion, LoadingState

logger = get_logger("autovideofactory.cv")


class OpenCVProcessor(ComputerVisionModuleInterface):
    def __init__(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED

    async def initialize(self, config: Optional[dict] = None) -> None:
        self._status = ModuleStatus.READY
        logger.info("OpenCV processor initialized")

    async def shutdown(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED

    async def health_check(self) -> ModuleHealth:
        return ModuleHealth(status=self._status, message="OpenCV ready" if self._status == ModuleStatus.READY else "Not ready")

    def get_capabilities(self):
        return [
            ModuleCapability(name="template_matching", description="Match visual templates in screenshots"),
            ModuleCapability(name="loading_detection", description="Detect loading states from screenshots"),
            ModuleCapability(name="element_detection", description="Detect UI elements visually"),
        ]

    async def find_template(
        self, screenshot: np.ndarray, template: np.ndarray, threshold: float = 0.8
    ) -> Optional[DetectedRegion]:
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                h, w = template.shape[:2]
                return DetectedRegion(
                    x=int(max_loc[0]),
                    y=int(max_loc[1]),
                    width=int(w),
                    height=int(h),
                    confidence=float(max_val),
                )
            return None
        except Exception as e:
            raise OCRVisionError(f"Template matching failed: {e}") from e

    async def detect_loading(self, screenshot: np.ndarray) -> LoadingState:
        try:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY) if len(screenshot.shape) == 3 else screenshot
            height, width = gray.shape

            spinner_region = gray[int(height * 0.4) : int(height * 0.6), int(width * 0.4) : int(width * 0.6)]

            blur = cv2.GaussianBlur(spinner_region, (5, 5), 0)
            edges = cv2.Canny(blur, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size

            brightness = np.mean(gray)
            brightness_change = 0.0

            return LoadingState(
                is_loading=edge_density > 0.1 or brightness < 30,
                progress=min(edge_density * 100, 100),
                detected_by="edge_density" if edge_density > 0.1 else "brightness",
            )
        except Exception as e:
            raise OCRVisionError(f"Loading detection failed: {e}") from e

    async def find_text_region(self, screenshot: np.ndarray, text: str) -> Optional[DetectedRegion]:
        try:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY) if len(screenshot.shape) == 3 else screenshot
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                if 0.2 < aspect_ratio < 10 and h > 10 and w > 20:
                    return DetectedRegion(x=x, y=y, width=w, height=h, label="text_region", confidence=0.5)
            return None
        except Exception as e:
            raise OCRVisionError(f"Text region detection failed: {e}") from e

    async def detect_button(self, screenshot: np.ndarray, label: str) -> Optional[DetectedRegion]:
        return await self.find_text_region(screenshot, label)

    async def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> float:
        try:
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            diff = cv2.absdiff(gray1, gray2)
            similarity = 1.0 - (np.sum(diff > 25) / diff.size)
            return float(similarity)
        except Exception as e:
            raise OCRVisionError(f"Image comparison failed: {e}") from e

    async def preprocess(self, image: np.ndarray) -> np.ndarray:
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            denoised = cv2.fastNlMeansDenoising(gray, h=30)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(denoised)
            return enhanced
        except Exception as e:
            raise OCRVisionError(f"Image preprocessing failed: {e}") from e
