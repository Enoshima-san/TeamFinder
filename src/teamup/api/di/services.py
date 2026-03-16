from src.teamup.application import AuthService

from .repositories import get_user_repository


async def get_auth_service() -> AuthService:
    return AuthService(await get_user_repository())
