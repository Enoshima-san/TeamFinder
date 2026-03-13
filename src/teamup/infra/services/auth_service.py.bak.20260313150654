from uuid import UUID

from src.teamup.application import IAuthService, IUserRepository
from src.teamup.core import logger
from src.teamup.domain import User
from src.teamup.schemas import LoginRequest, RegisterRequest, TokenData, TokenPair

from ..security import JWTHandler, PasswordHasher


class AuthService(IAuthService):
    """
    Класс авторизации пользователя, отвечающий за формирование JWT
    и внесение в базу новых пользователей.\n\n
    returns:
        `TokenPair` - объект-обёртка с данными для JWT
    """

    def __init__(self, user_repository: IUserRepository):
        logger.info("Инициализация AuthService")
        self.user_repository = user_repository

    async def register(self, req: RegisterRequest) -> TokenPair | None:
        """
        Регистрация пользователя с автоматическим входом в систему.\n
        При попытке ввести существующие данные базе, возвращает `None`.
        """
        if len(req.password.encode("utf-8")) > 72:
            raise ValueError("Пароль не должен превышать 72 байта")

        if await self.user_repository.check_new_user(req.email, req.username):
            logger.info("Пользователь с таким email или username уже существует")
            return None

        password_hash = PasswordHasher.hash(req.password)
        created_user = User(
            email=req.email,
            username=req.username,
            password_hash=password_hash,
        )

        created_user = await self.user_repository.create(created_user)
        if not created_user:
            logger.error("Не удалось создать пользователя")
            return None

        token_data = JWTHandler.get_token_data(
            created_user.user_id, created_user.username, created_user.role
        )

        return TokenPair(
            access_token=JWTHandler.create_access_token(token_data),
            refresh_token=JWTHandler.create_refresh_token(token_data),
        )

    async def login(self, req: LoginRequest) -> TokenPair | None:
        """
        Вход в систему существующих пользователей.\n
        При отсутствии совпададений вернёт `None`.
        """
        login_user = None
        if "@" in req.login:
            login_user = await self.user_repository.get_by_email(req.login)
        else:
            login_user = await self.user_repository.get_by_username(req.login)

        if not login_user:
            return None

        token_data = JWTHandler.get_token_data(
            login_user.user_id, login_user.username, login_user.role
        )

        return TokenPair(
            access_token=JWTHandler.create_access_token(token_data),
            refresh_token=JWTHandler.create_refresh_token(token_data),
        )

    async def refresh_tokens(self, token: str) -> TokenPair | None:
        """
        Обновление пары токенов по `refresh_token`.\n
        Вернёт новую пару или `None`
        """
        payload = JWTHandler.verify_token(token, "refresh")
        if not payload:
            return None

        user = await self.user_repository.get_by_id(UUID(payload["sub"]))
        if not user:
            return None

        token_data = JWTHandler.get_token_data(user.user_id, user.username, user.role)

        return TokenPair(
            access_token=JWTHandler.create_access_token(token_data),
            refresh_token=JWTHandler.create_refresh_token(token_data),
        )

    async def verify_access_token(self, token: str) -> TokenData | None:
        """
        Извдекает и проверяет токен из заголовка.
        Автоматически вызывается из-за `Depends()`
        """
        payload = JWTHandler.verify_token(token, "access")
        if not payload:
            return None
        return TokenData(
            user_id=UUID(payload["sub"]),
            username=payload["username"],
            role=payload["role"],
        )
