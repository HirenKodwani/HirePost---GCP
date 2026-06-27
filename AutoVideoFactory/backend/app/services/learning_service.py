from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Optional

from ..core.logging import get_logger

logger = get_logger("autovideofactory.services.learning")


class LearningService:
    def __init__(self) -> None:
        self._feedback_data: list[dict[str, Any]] = []
        self._prompt_performance: dict[str, list[float]] = defaultdict(list)

    async def record_feedback(
        self,
        input_data: dict[str, Any],
        output_data: dict[str, Any],
        feedback_score: float,
        source: str = "system",
    ) -> None:
        record = {
            "input": input_data,
            "output": output_data,
            "feedback_score": feedback_score,
            "source": source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._feedback_data.append(record)
        logger.info(f"Feedback recorded: {feedback_score:.2f} from {source}")

        prompt_key = input_data.get("prompt_type", "unknown")
        self._prompt_performance[prompt_key].append(feedback_score)

        if len(self._feedback_data) > 10000:
            self._feedback_data = self._feedback_data[-5000:]

    async def get_best_prompts(self, prompt_type: str, top_k: int = 5) -> list[dict[str, Any]]:
        scored = []
        for record in self._feedback_data:
            if record["input"].get("prompt_type") == prompt_type:
                scored.append({
                    "prompt": record["input"].get("prompt_text", ""),
                    "score": record["feedback_score"],
                    "output": record["output"],
                })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    async def get_insights(self) -> dict[str, Any]:
        avg_scores = {}
        for prompt_type, scores in self._prompt_performance.items():
            avg_scores[prompt_type] = sum(scores) / len(scores) if scores else 0.0

        return {
            "total_feedback_records": len(self._feedback_data),
            "average_scores_by_type": avg_scores,
            "best_performing_type": max(avg_scores, key=avg_scores.get) if avg_scores else None,
            "worst_performing_type": min(avg_scores, key=avg_scores.get) if avg_scores else None,
        }

    async def evolve_prompt(self, prompt_type: str, current_prompt: str) -> str:
        best = await self.get_best_prompts(prompt_type, 3)
        if not best:
            return current_prompt

        improvements = []
        for b in best:
            improvements.append(f"Score {b['score']:.2f}: {b['prompt'][:100]}")
        logger.info(f"Prompt evolution for {prompt_type}: {len(improvements)} candidates")
        return f"{current_prompt} [Optimized based on {len(improvements)} previous results]"

    async def get_recommendations(self, video_analytics: dict[str, Any]) -> list[str]:
        recommendations = []

        avg_watch = video_analytics.get("avg_watch_percentage", 0)
        if avg_watch < 50:
            recommendations.append("Improve hook in first 3 seconds")
        if avg_watch < 30:
            recommendations.append("Reduce video length")

        views = video_analytics.get("views", 0)
        if views < 100:
            recommendations.append("Optimize title and hashtags for discoverability")
            recommendations.append("Consider trending topics in your niche")

        return recommendations
