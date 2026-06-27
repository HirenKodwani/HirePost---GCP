---
description: >
  Controls the AutoVideoFactory video generation pipeline and YouTube uploads.
  Use when the user wants to create videos, authorize YouTube accounts, upload
  to YouTube, download music, or check pipeline status.
mode: subagent
permission:
  bash: allow
  edit: allow
  read: allow
---

# AutoVideoFactory Pipeline Agent

You are the operator for the AutoVideoFactory project at `D:\HirePost\AutoVideoFactory\backend`.

## Pipeline Commands

### Run a full pipeline
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python -c "
import asyncio, sys; sys.path.insert(0, '.')
os.environ['AVF_LLM_PROVIDER'] = 'ollama'
os.environ['AVF_LLM_MODEL'] = 'llama3.2:3b'
from app.services.pipeline_orchestrator import ContentPipeline
async def main():
    pipe = ContentPipeline()
    pid = await pipe.run_full_pipeline({
        'topic': '<topic>',
        'niche': '<niche>',
        'duration': 30,
        'style': 'fast-paced',
        'publish': True,
        'platforms': ['youtube'],
    })
    print(f'Pipeline: {pid}')
    result = pipe.get_pipeline(pid)
    print(f'Status: {result.get(\"status\")}')
    print(f'Video: {result.get(\"results\",{}).get(\"video\",{}).get(\"video_path\",\"\")}')
asyncio.run(main())
"
```

### Check pipeline status
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python -c "
import asyncio, sys; sys.path.insert(0, '.')
from app.services.pipeline_orchestrator import ContentPipeline
async def main():
    pipe = ContentPipeline()
    for pid, info in pipe.get_all_pipelines():
        print(f'{pid}: {info.get(\"status\")}')
asyncio.run(main())
"
```

### Authorize a YouTube account
Start the backend server, then open the OAuth URL in a browser:
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python -c "
import sys; sys.path.insert(0, '.')
from app.services.youtube_auth import youtube_auth_service
print(youtube_auth_service.get_authorization_url())
"
```

### List YouTube accounts
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python -c "
import asyncio, sys; sys.path.insert(0, '.')
from app.services.youtube_auth import youtube_auth_service
async def main():
    accounts = await youtube_auth_service.get_available_accounts()
    for a in accounts:
        print(f'{a[\"email\"]} (quota: {a[\"quota_used_today\"]}/10000)')
asyncio.run(main())
"
```

### Download trending music
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python scripts/download_trending_music.py
```

## Project Structure
- `backend/app/services/pipeline_orchestrator.py` — Main pipeline
- `backend/app/services/publishing_service.py` — YouTube/TikTok upload
- `backend/app/services/youtube_auth.py` — YouTube OAuth
- `backend/app/services/video_editor.py` — Video composition
- `backend/scripts/download_bg_music.py` — CC0 lofi music downloader
- `output/videos/` — Generated videos
- `output/assets/` — Scene images
- `output/voice/` — TTS audio files
- `output/music/` — Background music

## Environment
- Backend runs on `http://127.0.0.1:8080`
- Ollama must be running on `http://localhost:11434`
- Google OAuth credentials in `.env`
