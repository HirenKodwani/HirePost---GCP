from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, DatabaseEngine, get_db
from app.main import app


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_create_project(client):
    response = await client.post("/api/v1/projects/?name=Test+Project&description=Testing")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"


@pytest.mark.asyncio
async def test_list_projects(client):
    await client.post("/api/v1/projects/?name=Project+1")
    await client.post("/api/v1/projects/?name=Project+2")

    response = await client.get("/api/v1/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["projects"]) >= 2


@pytest.mark.asyncio
async def test_get_nonexistent_project(client):
    response = await client.get("/api/v1/projects/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_dashboard(client):
    response = await client.get("/api/v1/admin/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
    assert "recent_jobs" in data


@pytest.mark.asyncio
async def test_list_agents(client):
    response = await client.get("/api/v1/agents/")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
