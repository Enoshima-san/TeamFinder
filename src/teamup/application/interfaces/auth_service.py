```python
from abc import ABC, abstractmethod
from typing import Optional

from ...schemas import LoginRequest, RegisterRequest, TokenData, TokenPair


class IAuthService(ABC):
    """
    Interface for authentication services.
    """

    @abstractmethod
    async def register_user(self, registration_request: RegisterRequest) -> Optional[TokenPair]:
        """
        Registers a new user.

        Args:
            registration_request: The registration request.

        Returns:
            A token pair if registration is successful, otherwise None.
        """
        pass

    @abstractmethod
    async def authenticate_user(self, login_request: LoginRequest) -> Optional[TokenPair]:
        """
        Authenticates an existing user.

        Args:
            login_request: The login request.

        Returns:
            A token pair if authentication is successful, otherwise None.
        """
        pass

    @abstractmethod
    async def refresh_access_tokens(self, refresh_token: str) -> Optional[TokenPair]:
        """
        Refreshes access tokens.

        Args:
            refresh_token: The refresh token.

        Returns:
            A token pair if refresh is successful, otherwise None.
        """
        pass

    @abstractmethod
    async def verify_access_token(self, access_token: str) -> Optional[TokenData]:
        """
        Verifies an access token.

        Args:
            access_token: The access token.

        Returns:
            The token data if verification is successful, otherwise None.
        """
        pass
```