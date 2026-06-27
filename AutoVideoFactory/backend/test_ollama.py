import asyncio, httpx, time, sys, traceback

async def test():
    s = time.time()
    client = httpx.AsyncClient(timeout=300.0)
    try:
        print(f"Connecting to Ollama at {time.time()-s:.1f}s...", flush=True)
        r = await client.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:3b",
            "prompt": "Say hello in 3 words",
            "stream": False,
            "options": {"num_predict": 10},
        })
        print(f"Response received at {time.time()-s:.1f}s", flush=True)
        print(f"Status: {r.status_code}", flush=True)
        print(r.json()["response"], flush=True)
    except httpx.ReadTimeout:
        print(f"TIMEOUT after {time.time()-s:.1f}s", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        traceback.print_exc()
    finally:
        await client.aclose()

asyncio.run(test())
