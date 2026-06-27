"""
AutoVideoFactory Modules Package.

Each module follows Clean Architecture principles:
- Exposes an interface (ModuleInterface)
- Provides independent functionality
- Uses dependency injection
- Can be enabled/disabled independently
"""

from .base import (
    AgentInterface,
    BrowserProviderInterface,
    ConfigProviderInterface,
    ContentGenerationProviderInterface,
    ModuleCapability,
    ModuleHealth,
    ModuleInterface,
    ModuleStatus,
    ProviderInterface,
)

__all__ = [
    "AgentInterface",
    "BrowserProviderInterface",
    "ConfigProviderInterface",
    "ContentGenerationProviderInterface",
    "ModuleCapability",
    "ModuleHealth",
    "ModuleInterface",
    "ModuleStatus",
    "ProviderInterface",
]
