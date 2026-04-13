import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger
from teamup.infra.database import get_async_session
from teamup.schemas import LoginRequest, RegisterRequest, TokenPair, UserResponse

from ..di import get_auth_service

logger = get_logger()

auth_router = APIRouter(tags=["Auth"], prefix="/auth")


@auth_router.post(
    "/registration", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_async_session)):
    """
    Регистрация нового пользователя с автовходом
    и формированием JWT
    """
    auth_s = await get_auth_service(db)
    logger.info("Запрос на регистрацию.")
    user = await auth_s.register(req)
    res = UserResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        registration_date=user.registration_date,
        last_login=user.last_login,
        is_active=user.is_active,
        role=user.role,
        age=user.age,
        about_me=user.about_me,
    )
    await db.commit()
    return res


@auth_router.post("/login", response_model=TokenPair)
async def login(request: Request, db: AsyncSession = Depends(get_async_session)):
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

    auth_s = await get_auth_service(db)

    req = LoginRequest(login=login, password=password)

    access, refresh = await auth_s.login(req)
    res = TokenPair(access_token=access, refresh_token=refresh)

    logger.info("Успешная авторизация.")
    return res


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def refresh(req: dict, db: AsyncSession = Depends(get_async_session)):
    """Обновление пары токенов"""
    auth_s = await get_auth_service(db)
    token = req.get("refresh", None)
    if token is None:
        logger.error("Обновляющий токен не найден")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления токена: не указан токен",
        )
    access, refresh = await auth_s.refresh_tokens(token)
    res = TokenPair(access_token=access, refresh_token=refresh)
    return res


# @auth_router.post("/login", response_model=TokenPair)
# async def login(req: LoginRequest, db: AsyncSession = Depends(get_async_session)):
#     """
#     Авторизация пользователя и формирование JWT
#     """
#     auth_s = await get_auth_service(db)
#     access, refresh = await auth_s.login(req)
#     res = TokenPair(access_token=access, refresh_token=refresh)

#     return res
