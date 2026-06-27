"""Start uvicorn as subprocess and run API tests."""
import asyncio
import os
import subprocess
import sys
import time

import httpx


async def test():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8080", timeout=10) as c:
        for i in range(20):
            try:
                r = await c.get("/health")
                if r.status_code == 200:
                    break
            except Exception:
                await asyncio.sleep(1)
        else:
            print("Server not ready after 20s")
            return

        print(f"1. Health: {r.status_code} {r.json()}")

        r = await c.post("/api/v1/projects/", json={"name": "My First Video", "description": "Testing"})
        print(f"2. Create Project: {r.status_code} {r.text[:300]}")

        r = await c.get("/api/v1/projects/")
        print(f"3. List Projects: {r.status_code} count={r.json().get('projects', [])}")

        r = await c.get("/api/v1/admin/dashboard")
        data = r.json()
        print(f"4. Dashboard: {r.status_code} stats={data.get('stats', {})}")

        r = await c.get("/api/v1/agents/")
        print(f"5. Agents: {r.status_code} count={len(r.json().get('agents', []))}")

        r = await c.post(
            "/api/v1/agents/pipeline",
            json={"name": "test", "steps": [{"agent": "research", "action": "research_topic", "params": {}}]},
        )
        print(f"6. Pipeline: {r.status_code} {r.json()}")

        r = await c.get("/api/v1/system/config")
        cfg = r.json()
        print(f"7. Config: {r.status_code} app={cfg.get('app_name')} provider={cfg.get('llm_provider')}")

        print("\nALL TESTS PASSED")


if __name__ == "__main__":
    env = os.environ.copy()
    env["AVF_DATABASE_URL"] = "sqlite+aiosqlite:///./test_data/test.db"
    env["AVF_DEBUG"] = "false"
    env["AVF_LOG_LEVEL"] = "ERROR"

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080", "--log-level", "warning"],
        cwd=os.path.join(os.path.dirname(__file__)),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        asyncio.run(test())
    finally:
        proc.terminate()
        proc.wait(timeout=5)
