from uuid import UUID

from teamup.core import get_logger
from teamup.domain import IUserRepository, User
from teamup.infra import JWTHandler, PasswordHasher
from teamup.schemas import (
    JwtPayload,
    LoginRequest,
    RegisterRequest,
    TokenData,
    TokenPair,
    UserResponse,
)

from ..di import get_user_repository
from ..exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    PermissionDeniedError,
    UserAlreadyExistsError,
    UserCreationError,
)

logger = get_logger()


class AuthService:
    """
    Класс авторизации пользователя, отвечающий за формирование JWT
    и внесение в базу новых пользователей.
    """

    def __init__(self):
        logger.info("Инициализация AuthService")

    async def register(self, req: RegisterRequest) -> UserResponse:
        """
        Регистрация пользователя.

        Raises:
            - `UserAlreadyExistsError`: Если пользователь с таким email или username уже существует
            - `UserCreationError`: Если не удалось создать пользователя в БД

        Returns:
            `UserResponse`: Данные созданного пользователя
        """
        async with await get_user_repository() as user_repository:
            if await user_repository.check_new_user(req.email, req.username):
                logger.warning(
                    f"Попытка регистрации с существующим email или username: {req.email}"
                )
                raise UserAlreadyExistsError(
                    "Пользователь с таким email или username уже существует"
                )

            password_hash = PasswordHasher.hash(req.password)
            created_user = User.create(
                email=req.email,
                username=req.username,
                password_hash=password_hash,
            )

            created_user = await user_repository.create(created_user)
            if not created_user:
                logger.error(f"Не удалось создать пользователя: {req.email}")
                raise UserCreationError("Не удалось создать пользователя")

            logger.info(f"Пользователь {created_user.username} успешно зарегистрирован")

            return UserResponse(
                username=created_user.username,
                email=created_user.email,
                registration_date=created_user.registration_date,
                last_login=created_user.last_login,
                is_active=created_user.is_active,
                role=created_user.role,
                age=created_user.age,
                about_me=created_user.about_me,
            )

    async def login(self, req: LoginRequest) -> TokenPair:
        """
        Вход в систему существующих пользователей.

        Raises:
            - `UserNotFoundError`: Если пользователь не найден
            - `InvalidCredentialsError`: Если пароль неверный

        Returns:
            `TokenPair`: Пара access и refresh токенов
        """
        async with await get_user_repository() as user_repository:
            login_user = None
            if "@" in req.login:
                login_user = await user_repository.get_by_email(req.login)
            else:
                login_user = await user_repository.get_by_username(req.login)

            if not login_user:
                logger.warning(
                    f"Попытка входа с неверными учётными данными: {req.login}"
                )
                raise PermissionDeniedError("Пользователь не найден")

            if not PasswordHasher.verify(req.password, login_user.password_hash):
                logger.warning(
                    f"Неверный пароль для пользователя: {login_user.username}"
                )
                raise InvalidCredentialsError("Неверный пароль")

            token_data = JWTHandler.get_token_data(
                login_user.user_id, login_user.username, login_user.role
            )

            logger.info(f"Пользователь {login_user.username} успешно вошёл в систему")

            return TokenPair(
                access_token=JWTHandler.create_access_token(token_data),
                refresh_token=JWTHandler.create_refresh_token(token_data),
            )

    async def refresh_tokens(self, token: str) -> TokenPair:
        """
        Обновление пары токенов по `refresh_token`.

        Raises:
            - `InvalidTokenError`: Если токен невалиден или истёк
            - `UserNotFoundError`: Если пользователь не найден

        Returns:
            `TokenPair`: Новая пара access и refresh токенов
        """
        payload = JWTHandler.verify_token(token, "refresh")
        if not payload:
            logger.warning("Попытка обновления с невалидным refresh токеном")
            raise InvalidTokenError("Невалидный или истёкший токен")

        async with await get_user_repository() as user_repository:
            user = await user_repository.get_by_id(UUID(payload["sub"]))
            if not user:
                logger.warning(f"Пользователь с ID {payload['sub']} не найден")
                raise PermissionDeniedError("Пользователь не найден")

            token_data = JWTHandler.get_token_data(
                user.user_id, user.username, user.role
            )

            logger.info(f"Токены обновлены для пользователя {user.username}")

            return TokenPair(
                access_token=JWTHandler.create_access_token(token_data),
                refresh_token=JWTHandler.create_refresh_token(token_data),
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
            username=validated.username,
            role=validated.role,
            exp=validated.exp,
        )
