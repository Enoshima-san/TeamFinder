from fastapi import Request
from fastapi.responses import JSONResponse

from src.teamup.application import (
    AnnouncementCreationError,
    AnnouncementNotFoundError,
    AnnouncementUpdateError,
    ForbiddenError,
    GameNotFoundError,
    InvalidRankRangeError,
    UserNotFoundError,
)


async def announcement_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик всех исключений объявлений"""

    status_code_map = {
        AnnouncementNotFoundError: 404,
        GameNotFoundError: 404,
        UserNotFoundError: 401,
        ForbiddenError: 403,
        InvalidRankRangeError: 400,
        AnnouncementCreationError: 500,
        AnnouncementUpdateError: 500,
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
