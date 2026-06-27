from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from ..core.config import settings
from ..core.database import DatabaseEngine
from ..core.exceptions import PublishingError
from ..core.logging import get_logger
from ..models.content import YouTubeAccount

logger = get_logger("autovideofactory.services.youtube_auth")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

SESSIONS_DIR = Path(settings.sessions_dir) / "youtube"


class YouTubeAuthService:
    def __init__(self) -> None:
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def get_authorization_url(self, redirect_uri: str = "http://localhost:8080/auth/youtube/callback") -> str:
        if not settings.google_client_id or not settings.google_client_secret:
            raise PublishingError(
                "Google OAuth not configured. Set AVF_GOOGLE_CLIENT_ID and AVF_GOOGLE_CLIENT_SECRET",
                code="OAUTH_NOT_CONFIGURED",
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(SESSIONS_DIR.parent.parent / "client_secret_129756332718-12jhdvm99p12geokv0ne7tg4o84eeque.apps.googleusercontent.com.json"),
            SCOPES,
        )
        flow.redirect_uri = redirect_uri
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return auth_url

    async def exchange_code(self, code: str, redirect_uri: str = "http://localhost:8080/auth/youtube/callback") -> dict[str, Any]:
        import httpx
        if not settings.google_client_id or not settings.google_client_secret:
            raise PublishingError("Google OAuth not configured")

        token_data = {
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://oauth2.googleapis.com/token", data=token_data)
            if resp.status_code != 200:
                raise PublishingError(f"Token exchange failed: {resp.text}", code="OAUTH_TOKEN_FAILED")
            tokens = resp.json()

        refresh_token = tokens.get("refresh_token")
        if not refresh_token:
            raise PublishingError("No refresh_token returned.", code="OAUTH_NO_REFRESH_TOKEN")

        access_token = tokens["access_token"]
        expires_in = tokens.get("expires_in", 3600)
        token_expiry = datetime.fromtimestamp(datetime.now(timezone.utc).timestamp() + expires_in, tz=timezone.utc)

        userinfo = await self._get_userinfo(access_token)
        email = userinfo.get("email", "unknown")
        channel_name = userinfo.get("name", "")

        async with DatabaseEngine.get_session_factory()() as session:
            from sqlalchemy import select
            result = await session.execute(select(YouTubeAccount).where(YouTubeAccount.email == email))
            existing = result.scalar_one_or_none()
            if existing:
                existing.refresh_token = refresh_token
                existing.token_expiry = token_expiry
            else:
                session.add(YouTubeAccount(
                    email=email, channel_name=channel_name,
                    refresh_token=refresh_token, token_expiry=token_expiry, is_active=True))
            await session.commit()

        return {"success": True, "email": email, "channel_name": channel_name, "expires_at": token_expiry.isoformat()}

    async def _get_userinfo(self, access_token: str) -> dict[str, Any]:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if resp.status_code == 200:
                return resp.json()
        return {"email": "unknown", "name": "YouTube User"}

    async def get_credentials(
        self, account_id: Optional[str] = None
    ) -> Optional[Credentials]:
        async with DatabaseEngine.get_session_factory()() as session:
            from sqlalchemy import select
            if account_id:
                result = await session.execute(
                    select(YouTubeAccount).where(
                        YouTubeAccount.id == account_id,
                        YouTubeAccount.is_active == True,
                    )
                )
            else:
                result = await session.execute(
                    select(YouTubeAccount).where(YouTubeAccount.is_active == True)
                    .order_by(YouTubeAccount.upload_count.asc())
                )
            account = result.scalar_one_or_none()
            if not account:
                return None

            creds = Credentials(
                token=None,
                refresh_token=account.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.google_client_id,
                client_secret=settings.google_client_secret,
                scopes=SCOPES,
            )

            if creds.expired or not creds.valid:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.warning(
                        f"Token refresh failed for {account.email}: {e}"
                    )
                    account.is_active = False
                    await session.commit()
                    return None

            return creds

    async def get_available_accounts(self) -> list[dict[str, Any]]:
        async with DatabaseEngine.get_session_factory()() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(YouTubeAccount).where(YouTubeAccount.is_active == True)
            )
            accounts = result.scalars().all()
            return [
                {
                    "id": acc.id,
                    "email": acc.email,
                    "channel_name": acc.channel_name,
                    "quota_used_today": acc.quota_used_today,
                    "upload_count": acc.upload_count,
                    "last_upload_at": (
                        acc.last_upload_at.isoformat()
                        if acc.last_upload_at
                        else None
                    ),
                }
                for acc in accounts
            ]

    async def has_quota_available(self, account_id: str) -> bool:
        async with DatabaseEngine.get_session_factory()() as session:
            account = await session.get(YouTubeAccount, account_id)
            if not account:
                return False

            import datetime as dt
            today = dt.date.today().isoformat()
            if account.quota_reset_date != today:
                account.quota_used_today = 0
                account.quota_reset_date = today
                await session.commit()
                return True

            cost_per_upload = settings.google_youtube_upload_cost
            return account.quota_used_today + cost_per_upload <= settings.google_youtube_quota_per_account

    async def record_upload(self, account_id: str) -> None:
        import datetime as dt
        async with DatabaseEngine.get_session_factory()() as session:
            account = await session.get(YouTubeAccount, account_id)
            if account:
                today = dt.date.today().isoformat()
                if account.quota_reset_date != today:
                    account.quota_used_today = 0
                    account.quota_reset_date = today
                account.quota_used_today += settings.google_youtube_upload_cost
                account.upload_count += 1
                account.last_upload_at = datetime.now(timezone.utc)
                await session.commit()


youtube_auth_service = YouTubeAuthService()
