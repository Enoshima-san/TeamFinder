from uuid import UUID

from teamup.core import get_logger
from teamup.domain import IUserRepository, User
from teamup.infra import JWTHandler, PasswordHasher
from teamup.schemas import (
    JwtPayload,
    LoginRequest,
    RegisterRequest,
    TokenData,
)

from ..exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserCreationError,
    UserNotFoundError,
)

logger = get_logger()


class AuthService:
    """
    Класс авторизации пользователя, отвечающий за формирование JWT
    и внесение в базу новых пользователей.
    """

    def __init__(self, user_r: IUserRepository):
        logger.info("Инициализация AuthService")
        self._user_r = user_r

    async def register(self, req: RegisterRequest) -> User:
        """
        Регистрация пользователя.

        Raises:
            - `UserAlreadyExistsError`: Если пользователь с таким email или username уже существует
            - `UserCreationError`: Если не удалось создать пользователя в БД

        Returns:
            `User`: Доменная сущность пользователя
        """
        if await self._user_r.check_new_user(req.email, req.username):
            logger.warning(
                f"Попытка регистрации с существующим email или username: {req.email}"
            )
            raise UserAlreadyExistsError(
                "Пользователь с таким email или username уже существует"
            )

        password_hash = PasswordHasher.hash(req.password)
        user = User.create(
            email=req.email,
            username=req.username,
            password_hash=password_hash,
        )

        user = await self._user_r.create(user)
        if not user:
            logger.error(f"Не удалось создать пользователя: {req.email}")
            raise UserCreationError("Не удалось создать пользователя")

        logger.info(f"Пользователь {user.username} успешно зарегистрирован")

        return user

    async def login(self, req: LoginRequest) -> tuple[str, str]:
        """
        Вход в систему существующих пользователей.

        Raises:
            - `UserNotFoundError`: Если пользователь не найден
            - `InvalidCredentialsError`: Если пароль неверный

        Returns:
            `tuple[str, str`]: пара access и refresh токенов
        """
        login_user = None
        if "@" in req.login:
            login_user = await self._user_r.get_by_email(req.login)
        else:
            login_user = await self._user_r.get_by_username(req.login)

        if not login_user:
            logger.warning(f"Попытка входа с неверными учётными данными: {req.login}")
            raise InvalidCredentialsError("Пользователь не найден")

        if not PasswordHasher.verify(req.password, login_user.password_hash):
            logger.warning(f"Неверный пароль для пользователя: {login_user.username}")
            raise InvalidCredentialsError("Неверный пароль")

        token_data = JWTHandler.get_token_data(
            login_user.user_id, login_user.email, login_user.username, login_user.role
        )

        login_user.set_last_login()
        await self._user_r.update(login_user)

        logger.info(f"Пользователь {login_user.username} успешно вошёл в систему")

        return (
            JWTHandler.create_access_token(token_data),
            JWTHandler.create_refresh_token(token_data),
        )

    async def refresh_tokens(self, token: str) -> tuple[str, str]:
        """
        Обновление пары токенов по `refresh_token`.

        Raises:
            - `InvalidTokenError`: Если токен невалиден или истёк
            - `UserNotFoundError`: Если пользователь не найден

        Returns:
            `tuple[str, str]`: Обновленная пара access и refresh токенов
        """
        payload = JWTHandler.verify_token(token, "refresh")
        if not payload:
            logger.warning("Попытка обновления с невалидным refresh токеном")
            raise InvalidTokenError("Невалидный или истёкший токен")

        user = await self._user_r.get_by_id_light(UUID(payload["sub"]))
        if not user:
            logger.warning(f"Пользователь с ID {payload['sub']} не найден")
            raise UserNotFoundError("Пользователь больше не существует")

        token_data = JWTHandler.get_token_data(
            user.user_id, user.email, user.username, user.role
        )

        logger.info(f"Токены обновлены для пользователя {user.username}")

        return (
            JWTHandler.create_access_token(token_data),
            JWTHandler.create_refresh_token(token_data),
        )

    async def verify_access_token(self, token: str) -> TokenData:
        """
        Извлекает и проверяет access токен из заголовка.

        Raises:
            `InvalidTokenError`: Если токен невалиден или истёк

        Returns:
            `TokenData`: Данные из токена (user_id, username, role, exp)
        """
        payload = JWTHandler.verify_token(token, "access")
        if not payload:
            logger.warning("Попытка проверки невалидного access токена")
            raise InvalidTokenError("Невалидный или истёкший токен")

        validated = JwtPayload(**payload)

        logger.info(f"Access токен проверен для пользователя {validated.username}")

        return TokenData(
            user_id=UUID(validated.sub),
            email=validated.email,
            username=validated.username,
            role=validated.role,
            exp=validated.exp,
        )
