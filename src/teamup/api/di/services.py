from src.teamup.application import AnnouncementListingService, AuthService


async def get_auth_service() -> AuthService:
    return AuthService()


async def get_announcement_listing_service() -> AnnouncementListingService:
    return AnnouncementListingService()
