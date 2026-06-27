"""
Authorize a YouTube account for AutoVideoFactory uploads.

Usage:
    python scripts/authorize_youtube.py
"""

from __future__ import annotations

import os
import socket
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_auth_oauthlib.flow import InstalledAppFlow
from app.core.config import settings
from app.core.database import DatabaseEngine
from app.models.content import YouTubeAccount


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    if not settings.google_client_id or not settings.google_client_secret:
        print("ERROR: Set AVF_GOOGLE_CLIENT_ID and AVF_GOOGLE_CLIENT_SECRET in .env")
        sys.exit(1)

    import asyncio
    import httpx

    async def save_credentials(creds):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"},
            )
            userinfo = resp.json() if resp.status_code == 200 else {}

        email = userinfo.get("email", "unknown")
        name = userinfo.get("name", "YouTube User")
        token_expiry = creds.expiry or datetime.now(timezone.utc)

        await DatabaseEngine.create_all()
        async with DatabaseEngine.get_session_factory()() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(YouTubeAccount).where(YouTubeAccount.email == email)
            )
            existing = result.scalar_one_or_none()
            if existing:
                existing.refresh_token = creds.refresh_token
                existing.token_expiry = token_expiry
            else:
                account = YouTubeAccount(
                    email=email,
                    channel_name=name,
                    refresh_token=creds.refresh_token,
                    token_expiry=token_expiry,
                    is_active=True,
                )
                session.add(account)
            await session.commit()

        print(f"\n✅ YouTube Account Authorized!")
        print(f"   Email: {email}")
        print(f"   Channel: {name}")

    client_config = {
        "installed": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    port = find_free_port()
    print(f"Opening browser on http://127.0.0.1:{port} for YouTube authorization...")

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(
        host="127.0.0.1",
        port=port,
        open_browser=True,
        authorization_prompt_message="",
        success_message="✅ YouTube Account Authorized! You can close this window.",
    )

    if not creds or not creds.refresh_token:
        print("ERROR: No refresh token received.")
        sys.exit(1)

    asyncio.run(save_credentials(creds))


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

if __name__ == "__main__":
    main()
