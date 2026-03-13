from src.teamup.application import IAuthService
from src.teamup.infra import AuthService

from .repositories import get_user_repository


async def get_auth_service() -> IAuthService:
    return AuthService(await get_user_repository())
