import json

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.teamup.application import AuthService
from src.teamup.core import get_logger
from src.teamup.schemas import LoginRequest, RegisterRequest, UserResponse, TokenPair

from ..di import get_auth_service

logger = get_logger()

auth_router = APIRouter(tags=["Auth"], prefix="/auth")


@auth_router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
    req: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Регистрация нового пользователя с автовходом
    и формированием JWT
    """
    logger.info("Запрос на регистрацию.")
    res = await auth_service.register(req)
    return res


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def login(
    request: Request, auth_service: AuthService = Depends(get_auth_service)
):
    """
    Принимает и JSON (фронтенд), и Form Data (Swagger).
    """
    logger.info("Запрос на логин.")

    content_type = request.headers.get("Content-Type", "")
    body = await request.body()

    login = None
    password = None

    if "application/json" in content_type:
        data = json.loads(body)
        login = None if data.get("login") == "" else data.get("login")
        password = None if data.get("password") == "" else data.get("password")

    elif "application/x-www-form-urlencoded" in content_type:
        from urllib.parse import parse_qs

        form_data = parse_qs(body.decode())
        login = form_data.get("username", [None])[0]
        password = form_data.get("password", [None])[0]

    else:
        logger.error("Неподдерживаемый тип содержимого.")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Неподдерживаемый тип содержимого",
        )

    if login is None or password is None:
        logger.error("Не указаны логин или пароль")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Указаны не все поля",
        )

    req = LoginRequest(login=login, password=password)

    res = await auth_service.login(req)

    logger.info("Успешная авторизация.")
    return res


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def refresh(req: dict, auth_service: AuthService = Depends(get_auth_service)):
    """Обновление пары токенов"""
    token = req.get("refresh", None)
    if token is None:
        logger.error("Рефреш токен не найден")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления токена: не указан токен",
        )
    res = await auth_service.refresh_tokens(token)

    return res


# Основной метод логина на сервер, закомментирован, пока используется Swagger

# @auth_router.post("/login", response_model=TokenPair)
# async def login(
#     req: LoginRequest, auth_service: IAuthService = Depends(get_auth_service)
# ):
#     """
#     Авторизация пользователя и формирование JWT
#     """
#     token = await auth_service.login(req)
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Ошибка авторизации: неверный логин или пароль",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return token
