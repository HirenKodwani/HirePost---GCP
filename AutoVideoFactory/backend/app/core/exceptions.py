from __future__ import annotations

from typing import Any, Optional


class AutoVideoFactoryError(Exception):
    """Base exception for all AutoVideoFactory errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        code: str = "UNKNOWN_ERROR",
        details: Optional[dict[str, Any]] = None,
        original: Optional[Exception] = None,
    ) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        self.original = original
        super().__init__(self.message)


class ConfigurationError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Configuration error",
        code: str = "CONFIG_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class DatabaseError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Database error",
        code: str = "DB_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class BrowserError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Browser automation error",
        code: str = "BROWSER_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class BrowserSessionError(BrowserError):
    def __init__(
        self,
        message: str = "Browser session error",
        code: str = "SESSION_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class OCRVisionError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "OCR / Computer vision error",
        code: str = "CV_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class AIClientError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "AI client error",
        code: str = "AI_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class AIClientRateLimitError(AIClientError):
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        code: str = "RATE_LIMIT",
        retry_after: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, code, **kwargs)


class ContentGenerationError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Content generation error",
        code: str = "CONTENT_GEN_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class VideoProcessingError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Video processing error",
        code: str = "VIDEO_PROC_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class PublishingError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Publishing error",
        code: str = "PUBLISH_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class AgentError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Agent error",
        code: str = "AGENT_ERROR",
        agent_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.agent_name = agent_name
        super().__init__(message, code, **kwargs)


class OrchestrationError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Orchestration error",
        code: str = "ORCH_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class PluginError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Plugin error",
        code: str = "PLUGIN_ERROR",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)


class ProviderError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Provider error",
        code: str = "PROVIDER_ERROR",
        provider_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.provider_name = provider_name
        super().__init__(message, code, **kwargs)


class ValidationError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Validation error",
        code: str = "VALIDATION_ERROR",
        field: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.field = field
        super().__init__(message, code, **kwargs)


class ResourceNotFoundError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(message, code, **kwargs)


class SessionExpiredError(AutoVideoFactoryError):
    def __init__(
        self,
        message: str = "Session expired",
        code: str = "SESSION_EXPIRED",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, code, **kwargs)
