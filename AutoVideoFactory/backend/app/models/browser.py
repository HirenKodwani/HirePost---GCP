from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDMixin


class BrowserSession(UUIDMixin, TimestampMixin, Base):
    profile_name: Mapped[str] = mapped_column(String(255), nullable=False)
    browser_type: Mapped[str] = mapped_column(String(50), default="chromium")
    state_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cookies_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    storage_state_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    viewport_width: Mapped[int] = mapped_column(Integer, default=1280)
    viewport_height: Mapped[int] = mapped_column(Integer, default=720)


class Account(UUIDMixin, TimestampMixin, Base):
    platform: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    cookies_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    profile_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rate_limit_remaining: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rate_limit_reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Provider(UUIDMixin, TimestampMixin, Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    provider_type: Mapped[str] = mapped_column(String(100), nullable=False)
    api_base_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    api_key: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    priority: Mapped[int] = mapped_column(Integer, default=0)
    capabilities_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
