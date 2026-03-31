from fastapi import Request
from fastapi.responses import JSONResponse

from teamup.application.exceptions import (
    AnnouncementCreationError,
    AnnouncementNotFoundError,
    AnnouncementUpdateError,
    ForbiddenError,
    GameNotFoundError,
    InvalidCredentialsError,
    InvalidRankRangeError,
    InvalidTokenError,
    PasswordMismatchError,
    PermissionDeniedError,
    UserAlreadyExistsError,
    UserCreationError,
)


async def exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик всех исключений объявлений"""

    status_code_map = {
        # Announcements
        AnnouncementNotFoundError: 404,
        GameNotFoundError: 404,
        ForbiddenError: 403,
        InvalidRankRangeError: 400,
        AnnouncementCreationError: 500,
        AnnouncementUpdateError: 500,
        # Auth
        PermissionDeniedError: 401,
        UserAlreadyExistsError: 409,
        UserCreationError: 500,
        InvalidCredentialsError: 401,
        InvalidTokenError: 401,
        PasswordMismatchError: 401,
    }

    status_code = status_code_map.get(type(exc), 500)

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": str(exc),
            "status_code": status_code,
        },
    )
