from abc import ABC, abstractmethod

from ...schemas import LoginRequest, RegisterRequest, TokenData, TokenPair


class IAuthService(ABC):
    @abstractmethod
    async def register(self, req: RegisterRequest) -> TokenPair | None:
        pass

    @abstractmethod
    async def login(self, req: LoginRequest) -> TokenPair | None:
        pass

    @abstractmethod
    async def refresh_tokens(self, token: str) -> TokenPair | None:
        pass

    @abstractmethod
    async def verify_access_token(self, token: str) -> TokenData | None:
        pass
