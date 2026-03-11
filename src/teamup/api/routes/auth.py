from fastapi import APIRouter, Depends, HTTPException, status

from src.teamup.application import IAuthService
from src.teamup.schemas import LoginRequest, RegisterRequest, TokenPair

from ..di import get_auth_service

auth_router = APIRouter()


@auth_router.post(
    "/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED
)
async def register(
    req: RegisterRequest, auth_service: IAuthService = Depends(get_auth_service)
):
    """
    Регистрация нового пользователя с автовходом
    и формированием JWT
    """
    token = await auth_service.register(req)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка регистрации: указаны существующие имя пользователя и/или адрес электронной почты",
        )
    return token


@auth_router.post("/login", response_model=TokenPair)
async def login(
    req: LoginRequest, auth_service: IAuthService = Depends(get_auth_service)
):
    """
    Авторизация пользователя и формирование JWT
    """
    token = await auth_service.login(req)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка авторизации: неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@auth_router.post("/refresh", response_model=TokenPair)
async def refresh(req: dict, auth_service: IAuthService = Depends(get_auth_service)):
    """Обновление пары токенов"""
    token = req.get("refresh")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления токена: не указан токен",
        )
    token_pair = await auth_service.refresh_tokens(token)
    if not token_pair:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка обновления токена: неверный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_pair
