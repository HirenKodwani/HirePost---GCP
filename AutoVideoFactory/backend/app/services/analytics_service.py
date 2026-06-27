from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from ..core.logging import get_logger
from ..models.analytics import AnalyticsEvent, Metric

logger = get_logger("autovideofactory.services.analytics")


class AnalyticsService:
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []
        self._metrics: dict[str, list[float]] = {}

    async def track_event(
        self,
        event_type: str,
        data: dict[str, Any],
        source: Optional[str] = None,
        video_id: Optional[str] = None,
        job_id: Optional[str] = None,
    ) -> None:
        event = {
            "event_type": event_type,
            "source": source or "system",
            "data": data,
            "video_id": video_id,
            "job_id": job_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._events.append(event)
        logger.info(f"Analytics event: {event_type}", extra=data)

        if len(self._events) > 10000:
            self._events = self._events[-5000:]

    async def record_metric(self, metric_name: str, value: float, tags: Optional[dict] = None) -> None:
        if metric_name not in self._metrics:
            self._metrics[metric_name] = []
        self._metrics[metric_name].append(value)
        if len(self._metrics[metric_name]) > 1000:
            self._metrics[metric_name] = self._metrics[metric_name][-500:]

    async def get_video_stats(self, video_id: str) -> dict[str, Any]:
        video_events = [e for e in self._events if e.get("video_id") == video_id]
        return {
            "video_id": video_id,
            "total_events": len(video_events),
            "views": sum(1 for e in video_events if e["event_type"] == "video.view"),
            "likes": sum(1 for e in video_events if e["event_type"] == "video.like"),
            "shares": sum(1 for e in video_events if e["event_type"] == "video.share"),
            "comments": sum(1 for e in video_events if e["event_type"] == "video.comment"),
        }

    async def get_metric_average(self, metric_name: str, period_hours: int = 24) -> float:
        values = self._metrics.get(metric_name, [])
        if not values:
            return 0.0
        return sum(values) / len(values)

    async def generate_report(self, period_days: int = 7) -> dict[str, Any]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=period_days)
        period_events = [
            e for e in self._events
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]

        event_counts: dict[str, int] = {}
        for e in period_events:
            et = e["event_type"]
            event_counts[et] = event_counts.get(et, 0) + 1

        return {
            "period_days": period_days,
            "total_events": len(period_events),
            "events_by_type": event_counts,
            "metrics": {k: sum(v) / len(v) if v else 0 for k, v in self._metrics.items()},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
