from __future__ import annotations

import base64
import io
from typing import Any, Optional

import numpy as np
from PIL import Image

from ...core.config import settings
from ...core.exceptions import BrowserError
from ...core.logging import get_logger
from ..ocr.engine import TesseractEngine
from .engine import PlaywrightBrowserEngine

logger = get_logger("autovideofactory.browser.computer_use")


class ComputerUseAgent:
    def __init__(
        self,
        browser_engine: Optional[PlaywrightBrowserEngine] = None,
        ocr_engine: Optional[TesseractEngine] = None,
    ) -> None:
        self._browser = browser_engine or PlaywrightBrowserEngine()
        self._ocr = ocr_engine or TesseractEngine()
        self._max_actions = settings.browser_use_max_actions
        self._action_count = 0

    async def initialize(self) -> None:
        await self._browser.initialize()
        await self._ocr.initialize()
        await self._browser.launch(headless=settings.browser_headless)
        logger.info("Computer Use Agent initialized")

    async def shutdown(self) -> None:
        await self._browser.shutdown()

    async def navigate_and_interact(self, url: str, actions: list[dict]) -> dict[str, Any]:
        result = await self._browser.navigate(url)
        if not result.success:
            return {"success": False, "error": result.error}

        for action in actions:
            if self._action_count >= self._max_actions:
                break

            action_type = action.get("type", "wait")
            try:
                if action_type == "click":
                    selector = action.get("selector", "")
                    await self._browser.click(selector)
                elif action_type == "type":
                    await self._browser.type_text(action["selector"], action["text"])
                elif action_type == "wait":
                    await self._browser.wait_for_selector(action.get("selector", "body"))
                elif action_type == "upload":
                    await self._browser.upload_file(action["selector"], action["file_path"])
                elif action_type == "screenshot":
                    screenshot = await self._browser.screenshot()
                    np_array = np.array(Image.open(io.BytesIO(screenshot)))
                    ocr_result = await self._ocr.extract_text(np_array)
                    logger.info(f"OCR text found: {ocr_result.text[:100]}")
                elif action_type == "scroll":
                    await self._browser.scroll(action.get("direction", "down"), action.get("amount", 300))
                elif action_type == "wait_for_navigation":
                    await self._browser.wait_for_navigation()

                self._action_count += 1
            except Exception as e:
                logger.error(f"Action {action_type} failed: {e}")
                return {"success": False, "action": action_type, "error": str(e)}

        return {"success": True, "actions_taken": self._action_count}

    async def ai_navigate(self, url: str, objective: str) -> dict[str, Any]:
        logger.info(f"AI navigating to {url} with objective: {objective}")

        nav_result = await self._browser.navigate(url)
        if not nav_result.success:
            return {"success": False, "error": nav_result.error}

        screenshot = await self._browser.screenshot()
        np_array = np.array(Image.open(io.BytesIO(screenshot)))
        ocr_result = await self._ocr.extract_text(np_array)

        page_text = ocr_result.text
        page_html = await self._browser.get_html()

        return {
            "success": True,
            "page_text": page_text[:500],
            "elements": ocr_result.regions[:20],
            "url": url,
            "objective": objective,
        }

    async def detect_and_handle_loading(self) -> bool:
        screenshot = await self._browser.screenshot()
        np_array = np.array(Image.open(io.BytesIO(screenshot)))
        from ..computer_vision.processor import OpenCVProcessor
        cv = OpenCVProcessor()
        loading_state = await cv.detect_loading(np_array)
        if loading_state.is_loading:
            logger.info("Loading state detected, waiting...")
            import asyncio
            await asyncio.sleep(2)
            return True
        return False
