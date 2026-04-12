from fastapi import Request
from fastapi.responses import JSONResponse

from teamup.application.exceptions import (
    AnnouncementCreationError,
    AnnouncementDeleteError,
    AnnouncementNotFoundError,
    AnnouncementUpdateError,
    ExternalApiError,
    ForbiddenError,
    GameNotFoundError,
    InvalidCredentialsError,
    InvalidRankRangeError,
    InvalidTokenError,
    PasswordMismatchError,
    PermissionDeniedError,
    ResponseCreationError,
    ResponseDeletionError,
    ResponseNotFoundError,
    UnauthorizedError,
    UserAlreadyExistsError,
    UserCreationError,
    UserGameCreationError,
    UserNotFoundError,
)


async def exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик всех исключений объявлений"""
    status_code_map = {
        # Not Found
        AnnouncementNotFoundError: 404,
        AnnouncementDeleteError: 404,
        GameNotFoundError: 404,
        ResponseNotFoundError: 404,
        UserNotFoundError: 404,
        # Forbidden / Permission
        ForbiddenError: 403,
        PermissionDeniedError: 403,
        # Bad Request
        InvalidRankRangeError: 400,
        # Conflict
        UserAlreadyExistsError: 409,
        # Unauthorized / Auth
        InvalidCredentialsError: 401,
        InvalidTokenError: 401,
        PasswordMismatchError: 401,
        UnauthorizedError: 401,
        # Server Errors
        AnnouncementCreationError: 500,
        AnnouncementUpdateError: 500,
        UserCreationError: 500,
        UserGameCreationError: 500,
        ResponseCreationError: 500,
        ResponseDeletionError: 500,
        # External API
        ExternalApiError: 400,
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
