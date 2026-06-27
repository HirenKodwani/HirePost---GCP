from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.logging import get_logger
from ...models.project import Project

logger = get_logger("autovideofactory.api.projects")
router = APIRouter()


@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    projects = result.scalars().all()
    return {"projects": [{"id": p.id, "name": p.name, "status": p.status, "created_at": str(p.created_at)} for p in projects]}


@router.post("/")
async def create_project(data: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = data.get("name", "Untitled")
    description = data.get("description", "")
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"id": project.id, "name": project.name, "status": project.status}


@router.get("/{project_id}")
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": {"id": project.id, "name": project.name, "status": project.status, "description": project.description, "created_at": str(project.created_at)}}


@router.delete("/{project_id}")
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    await db.commit()
    return {"deleted": True}
