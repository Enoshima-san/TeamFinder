from src.teamup.application import AnnouncementListingService, AuthService

from .repositories import (
    get_announcement_repository,
    get_game_repository,
    get_user_repository,
)


async def get_auth_service() -> AuthService:
    return AuthService(await get_user_repository())


async def get_announcement_listing_service() -> AnnouncementListingService:
    return AnnouncementListingService(
        await get_announcement_repository(),
        await get_user_repository(),
        await get_game_repository(),
    )
