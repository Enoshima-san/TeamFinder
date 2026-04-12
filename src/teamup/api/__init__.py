from .di import get_auth_service, get_current_user
from .exception_handlers import exception_handler
from .external import external_router
from .routes import (
    auth_router,
    feed_router,
    games_router,
    responses_router,
    user_router,
)

__all__ = [
    "auth_router",
    "feed_router",
    "get_auth_service",
    "get_current_user",
    "exception_handler",
    "responses_router",
    "games_router",
    "user_router",
    "external_router",
]
