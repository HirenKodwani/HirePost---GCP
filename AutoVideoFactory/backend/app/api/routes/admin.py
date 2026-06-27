from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.logging import get_logger
from ...models.job import Job, Run
from ...models.project import Project

logger = get_logger("autovideofactory.api.admin")
router = APIRouter()


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)):
    total_projects = (await db.execute(select(func.count(Project.id)))).scalar()
    total_jobs = (await db.execute(select(func.count(Job.id)))).scalar()
    active_jobs = (await db.execute(select(func.count(Job.id)).where(Job.status == "running"))).scalar()
    failed_jobs = (await db.execute(select(func.count(Job.id)).where(Job.status == "failed"))).scalar()
    completed_jobs = (await db.execute(select(func.count(Job.id)).where(Job.status == "completed"))).scalar()

    recent_jobs_result = await db.execute(select(Job).order_by(Job.created_at.desc()).limit(10))
    recent_jobs = recent_jobs_result.scalars().all()

    return {
        "stats": {
            "total_projects": total_projects or 0,
            "total_jobs": total_jobs or 0,
            "active_jobs": active_jobs or 0,
            "failed_jobs": failed_jobs or 0,
            "completed_jobs": completed_jobs or 0,
        },
        "recent_jobs": [
            {
                "id": j.id,
                "job_type": j.job_type,
                "status": j.status,
                "progress": j.progress,
                "created_at": str(j.created_at),
            }
            for j in recent_jobs
        ],
    }


@router.get("/logs")
async def get_logs(level: str = "", limit: int = 100, db: AsyncSession = Depends(get_db)):
    from ...models.job import Log
    query = select(Log).order_by(Log.timestamp.desc()).limit(limit)
    if level:
        query = query.where(Log.level == level.upper())
    result = await db.execute(query)
    logs = result.scalars().all()
    return {
        "logs": [
            {
                "id": log.id,
                "level": log.level,
                "message": log.message,
                "logger_name": log.logger_name,
                "timestamp": str(log.timestamp),
            }
            for log in logs
        ]
    }
