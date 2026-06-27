from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.logging import get_logger
from ...models.job import Job, Log

logger = get_logger("autovideofactory.api.jobs")
router = APIRouter()


@router.get("/")
async def list_jobs(status: str = "", db: AsyncSession = Depends(get_db)):
    query = select(Job).order_by(Job.created_at.desc())
    if status:
        query = query.where(Job.status == status)
    result = await db.execute(query)
    jobs = result.scalars().all()
    return {
        "jobs": [
            {
                "id": j.id,
                "job_type": j.job_type,
                "status": j.status,
                "progress": j.progress,
                "created_at": str(j.created_at),
            }
            for j in jobs
        ]
    }


@router.get("/{job_id}")
async def get_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job": {
            "id": job.id,
            "job_type": job.job_type,
            "status": job.status,
            "progress": job.progress,
            "progress_message": job.progress_message,
            "created_at": str(job.created_at),
            "started_at": str(job.started_at) if job.started_at else None,
            "completed_at": str(job.completed_at) if job.completed_at else None,
        }
    }


@router.post("/{job_id}/cancel")
async def cancel_job(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_cancellable:
        raise HTTPException(status_code=400, detail="Job cannot be cancelled")
    job.status = "cancelled"
    await db.commit()
    return {"cancelled": True}


@router.get("/{job_id}/logs")
async def get_job_logs(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Log).where(Log.job_id == job_id).order_by(Log.timestamp.asc())
    )
    logs = result.scalars().all()
    return {
        "logs": [
            {
                "id": log.id,
                "level": log.level,
                "message": log.message,
                "timestamp": str(log.timestamp),
            }
            for log in logs
        ]
    }
