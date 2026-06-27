from __future__ import annotations

from datetime import datetime, timezone

from app.models.base import Base
from app.models.project import Project, Script, Topic
from app.models.job import Job
from app.models.content import Video


class TestModels:
    def test_project_creation(self):
        project = Project(name="Test Project", description="A test project")
        assert project.name == "Test Project"
        assert project.status == "draft"
        assert project.id is not None
        assert len(project.id) == 32

    def test_project_timestamps(self):
        project = Project(name="Timestamps Test")
        assert project.created_at is not None
        assert project.updated_at is not None

    def test_job_defaults(self):
        job = Job(job_type="video_generation")
        assert job.status == "pending"
        assert job.priority == 0
        assert job.progress == 0.0
        assert job.retry_count == 0
        assert job.max_retries == 3
        assert job.is_cancellable is True

    def test_video_defaults(self):
        video = Video(project_id="test", title="Test Video")
        assert video.status == "draft"
        assert video.quality_score == 0.0
        assert video.is_published is False
        assert video.width == 1080
        assert video.height == 1920
        assert video.fps == 30.0

    def test_tablename_generation(self):
        assert Project.__tablename__ == "project"
        assert Script.__tablename__ == "script"
        assert Topic.__tablename__ == "topic"
        assert Video.__tablename__ == "video"
