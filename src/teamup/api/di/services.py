from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application import (
    AddGameUseCase,
    AnnouncementService,
    AuthService,
    GamesService,
    ResponsesService,
)
from teamup.application.use_cases import (
    GetFullUserUseCase,
    GetTopPlayersUseCase,
    GetUserGamesUseCase,
    GetUserUseCase,
)

from .repositories import (
    get_announcement_repository,
    get_game_repository,
    get_response_repository,
    get_user_games_repository,
    get_user_repository,
)


async def get_auth_service(db: AsyncSession) -> AuthService:
    return AuthService(await get_user_repository(db))


async def get_announcement_service(
    db: AsyncSession,
) -> AnnouncementService:
    return AnnouncementService(await get_announcement_repository(db))


async def get_responses_service(db: AsyncSession) -> ResponsesService:
    return ResponsesService(await get_response_repository(db))


async def get_games_service(db: AsyncSession) -> GamesService:
    return GamesService(await get_game_repository(db))


async def get_add_game_use_case(db: AsyncSession) -> AddGameUseCase:
    return AddGameUseCase(await get_user_games_repository(db))


async def get_full_user_info_use_case(db: AsyncSession) -> GetFullUserUseCase:
    return GetFullUserUseCase(await get_user_repository(db))


async def get_user_use_case(db: AsyncSession) -> GetUserUseCase:
    return GetUserUseCase(await get_user_repository(db))


async def get_user_games_use_case(db: AsyncSession) -> GetUserGamesUseCase:
    return GetUserGamesUseCase(
        await get_user_games_repository(db), await get_game_repository(db)
    )


async def get_top_players_use_case(game_name: str) -> GetTopPlayersUseCase:
    return GetTopPlayersUseCase(game_name)
