```python
from uuid import UUID
from typing import Optional

from src.teamup.application import IAuthService, IUserRepository
from src.teamup.core import logger
from src.teamup.domain import User
from src.teamup.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenData,
    TokenPair,
)

from ..security import JWTHandler, PasswordHasher


class AuthService(IAuthService):
    """
    Service class responsible for user authentication and token management.
    """

    def __init__(self, user_repository: IUserRepository):
        """
        Initializes the AuthService instance.

        Args:
            user_repository (IUserRepository): User repository instance.
        """
        logger.info("Initializing AuthService")
        self.user_repository = user_repository

    async def register_user(
        self, register_request: RegisterRequest
    ) -> Optional[TokenPair]:
        """
        Registers a new user with automatic login.

        Args:
            register_request (RegisterRequest): User registration request.

        Returns:
            TokenPair: Token pair for the newly created user or None if user already exists.
        """
        if len(register_request.password.encode("utf-8")) > 72:
            raise ValueError("Password should not exceed 72 bytes")

        if await self.user_repository.check_new_user(register_request.email, register_request.username):
            logger.info("User with this email or username already exists")
            return None

        password_hash = PasswordHasher.hash(register_request.password)
        created_user = User(
            email=register_request.email,
            username=register_request.username,
            password_hash=password_hash,
        )

        created_user = await self.user_repository.create(created_user)
        if not created_user:
            logger.error("Failed to create user")
            return None

        token_data = JWTHandler.get_token_data(
            created_user.user_id, created_user.username, created_user.role
        )

        return TokenPair(
            access_token=JWTHandler.create_access_token(token_data),
            refresh_token=JWTHandler.create_refresh_token(token_data),
        )

    async def login_user(self, login_request: LoginRequest) -> Optional[TokenPair]:
        """
        Logs in an existing user.

        Args:
            login_request (LoginRequest): User login request.

        Returns:
            TokenPair: Token pair for the logged-in user or None if login credentials are invalid.
        """
        login_user = None
        if "@" in login_request.login:
            login_user = await self.user_repository.get_by_email(login_request.login)
        else:
            login_user = await self.user_repository.get_by_username(login_request.login)

        if not login_user:
            return None

        token_data = JWTHandler.get_token_data(
            login_user.user_id, login_user.username, login_user.role
        )

        return TokenPair(
            access_token=JWTHandler.create_access_token(token_data),
            refresh_token=JWTHandler.create_refresh_token(token_data),
        )

    async def refresh_tokens(self, refresh_token: str) -> Optional[TokenPair]:
        """
        Refreshes the token pair using the refresh token.

        Args:
            refresh_token (str): Refresh token to use for refreshing.

        Returns:
            TokenPair: New token pair or None if refresh token is invalid.
        """
        payload = JWTHandler.verify_token(refresh_token, "refresh")
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

    async def verify_access_token(self, token: str) -> Optional[TokenData]:
        """
        Verifies and extracts the token from the request headers.

        Args:
            token (str): Access token to verify.

        Returns:
            TokenData: Token data or None if token is invalid.
        """
        payload = JWTHandler.verify_token(token, "access")
        if not payload:
            return None
        return TokenData(
            user_id=UUID(payload["sub"]),
            username=payload["username"],
            role=payload["role"],
        )
```