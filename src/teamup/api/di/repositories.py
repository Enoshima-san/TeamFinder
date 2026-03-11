from ...application import IUserRepository
from ...infra import UserRepository


async def get_user_repository() -> IUserRepository:
    return UserRepository()
