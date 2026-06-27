from __future__ import annotations

from fastapi import APIRouter

from .routes import admin, agents, auth, jobs, projects, system

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(system.router, prefix="/system", tags=["System"])
