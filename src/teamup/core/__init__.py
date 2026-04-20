from .logging import get_logger, setup_logging
from .settings import get_settings, settings

setup_logging()

__all__ = [
    "settings",
    "get_settings",
    "get_logger",
]
