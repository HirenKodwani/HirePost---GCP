from __future__ import annotations

from typing import Any, Optional

import numpy as np
import pytesseract
from PIL import Image

from ...core.config import settings
from ...core.exceptions import OCRVisionError
from ...core.logging import get_logger
from ..base import ModuleHealth, ModuleStatus
from . import OCRModuleInterface, OCRResult

logger = get_logger("autovideofactory.ocr")


class TesseractEngine(OCRModuleInterface):
    def __init__(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED

    async def initialize(self, config: Optional[dict] = None) -> None:
        try:
            pytesseract.get_tesseract_version()
            self._status = ModuleStatus.READY
            logger.info("Tesseract OCR engine initialized")
        except Exception as e:
            self._status = ModuleStatus.ERROR
            raise OCRVisionError(f"Tesseract not found: {e}. Install tesseract-ocr.") from e

    async def shutdown(self) -> None:
        self._status = ModuleStatus.UNINITIALIZED

    async def health_check(self) -> ModuleHealth:
        return ModuleHealth(status=self._status, message="OCR ready" if self._status == ModuleStatus.READY else "Not ready")

    def get_capabilities(self):
        return [
            ModuleCapability(name="text_extraction", description="Extract text from images using OCR", supported_providers=["tesseract"]),
            ModuleCapability(name="text_search", description="Search for specific text in images"),
        ]

    async def extract_text(self, image: np.ndarray, language: str = "eng") -> OCRResult:
        try:
            pil_image = Image.fromarray(image)
            ocr_data = pytesseract.image_to_data(pil_image, lang=language, output_type=pytesseract.Output.DICT)

            text = " ".join([t for t in ocr_data["text"] if t.strip()])
            confidences = [int(c) for c in ocr_data["conf"] if c > 0]
            avg_confidence = float(np.mean(confidences)) / 100.0 if confidences else 0.0

            regions = []
            for i in range(len(ocr_data["text"])):
                if ocr_data["text"][i].strip() and int(ocr_data["conf"][i]) > int(settings.ocr_confidence_threshold * 100):
                    regions.append({
                        "text": ocr_data["text"][i],
                        "x": ocr_data["left"][i],
                        "y": ocr_data["top"][i],
                        "width": ocr_data["width"][i],
                        "height": ocr_data["height"][i],
                        "confidence": int(ocr_data["conf"][i]) / 100.0,
                    })

            return OCRResult(text=text, confidence=avg_confidence, regions=regions)
        except Exception as e:
            raise OCRVisionError(f"OCR text extraction failed: {e}") from e

    async def find_text(self, image: np.ndarray, target_text: str) -> Optional[dict[str, Any]]:
        result = await self.extract_text(image)
        for region in result.regions:
            if target_text.lower() in region["text"].lower():
                return region
        return None

    async def extract_structured(self, image: np.ndarray, schema: dict[str, Any]) -> dict[str, Any]:
        result = await self.extract_text(image)
        extracted = {}
        for field_name, keywords in schema.items():
            for keyword in keywords if isinstance(keywords, list) else [keywords]:
                if keyword.lower() in result.text.lower():
                    extracted[field_name] = keyword
                    break
        return extracted

    async def detect_language(self, image: np.ndarray) -> str:
        try:
            pil_image = Image.fromarray(image)
            osd = pytesseract.image_to_osd(pil_image)
            for line in osd.split("\n"):
                if "Script:" in line:
                    return line.split(":")[-1].strip()
            return "unknown"
        except Exception as e:
            raise OCRVisionError(f"Language detection failed: {e}") from e
