from __future__ import annotations

from fastapi import APIRouter

from ...core.config import settings
from ...core.database import DatabaseEngine
from ...core.logging import get_logger

logger = get_logger("autovideofactory.api.system")
router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.environment.value,
        "database": "connected",
    }


@router.get("/config")
async def get_config():
    return settings.model_dump(exclude={"auth_jwt_secret", "llm_api_key", "openai_api_key"})


@router.get("/stats")
async def get_system_stats():
    import psutil
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }
