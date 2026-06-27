# AutoVideoFactory

> Enterprise-grade autonomous AI video generation platform. Local-first. Modular. Extensible.

## Architecture

AutoVideoFactory uses a clean architecture with strict separation of concerns:

- **Backend**: Python FastAPI with SQLAlchemy, Playwright, OpenCV, Tesseract OCR
- **Frontend**: Next.js 14 with TailwindCSS, shadcn/ui
- **Desktop**: Electron packaging (planned)
- **Database**: SQLite (default), PostgreSQL supported

### Module System

Every capability is an independent module exposing interfaces. Modules communicate through dependency injection, not direct imports.

### Multi-Agent System

18 specialized agents coordinated by an Agent Orchestrator:

| Agent | Role |
|-------|------|
| Planner | Pipeline planning and step decomposition |
| Trend | Trend discovery and analysis |
| Research | Topic research and fact-checking |
| Script | Script and scene writing |
| Prompt | Prompt engineering for AI models |
| Voice | TTS and voice cloning |
| Visual | Image generation |
| Video | Video generation |
| Editing | Video composition and effects |
| Subtitle | Speech-to-text and subtitle formatting |
| Publishing | Multi-platform publishing |
| Analytics | Performance analytics collection |
| Learning | Feedback-driven improvement |
| QA | Quality assurance checks |
| Recovery | Failure recovery and retry strategies |
| Browser | Browser automation |
| Supervisor | System supervision and health checks |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- FFmpeg
- Tesseract OCR
- Playwright (with Chromium)

### Backend

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --port 8080
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up -d
```

## Project Structure

```
autovideofactory/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, DB, logging, events
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── modules/       # Domain modules (30+)
│   │   ├── agents/        # Multi-agent system (18 agents)
│   │   ├── schemas/       # Pydantic schemas
│   │   └── api/           # FastAPI routes
│   ├── tests/
│   └── alembic/
├── frontend/
│   └── src/
│       └── app/           # Next.js pages
├── docker/
└── docs/
```

## Pipeline

```
Trend Discovery → Research → Script → Scene Planning →
Prompt Generation → Image/Video Generation → Voice →
Music → Subtitles → Editing → Brand Overlay →
Thumbnail → Metadata → Quality Review → Publishing →
Analytics → Learning
```

## License

MIT
