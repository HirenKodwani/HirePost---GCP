---
name: autovideofactory
description: |
  Use ONLY when working with the AutoVideoFactory project at D:\HirePost\AutoVideoFactory.
  This skill provides context on the full video generation pipeline: topic research,
  script writing, voiceover generation, image asset creation, Ken Burns video
  composition, YouTube upload, and background music management.
---

# AutoVideoFactory Skill

## Project Location
`D:\HirePost\AutoVideoFactory\backend` — Python FastAPI backend

## Key Architecture
- **Pipeline**: 12-step sequential/parallel pipeline in `pipeline_orchestrator.py`
- **Video**: PIL + numpy Ken Burns effect, FFmpeg composition
- **Voice**: edge-tts with mood-based voice/pitch/rate mapping
- **Images**: Pollinations.ai API (free, no key needed)
- **Music**: Local CC0 tracks in `output/music/` organized by mood
- **Publishing**: YouTube Data API + browser automation fallback

## Quick Start
```powershell
cd D:\HirePost\AutoVideoFactory\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

## Environment Variables (in backend/.env)
- `AVF_LLM_PROVIDER=ollama` — LLM backend
- `AVF_GOOGLE_CLIENT_ID` / `AVF_GOOGLE_CLIENT_SECRET` — YouTube OAuth

## Common Tasks
See the `pipeline-agent` for runnable commands. Key agents:
- `pipeline-agent` — Run pipeline, check status, YouTube management
- Use `explore` agent for codebase questions
