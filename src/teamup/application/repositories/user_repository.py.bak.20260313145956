from abc import ABC, abstractmethod
from uuid import UUID

from ...domain import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User | None:
        pass

    @abstractmethod
    async def delete(self, user: int | User) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User | None:
        pass

    @abstractmethod
    async def check_new_user(self, email: str, username: str) -> bool:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User | None:
        pass
