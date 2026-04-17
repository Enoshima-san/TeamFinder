from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.services import (
    AnnouncementService,
    AuthService,
    GamesService,
    ResponsesService,
)
from teamup.application.use_cases import (
    AddGameUseCase,
    CheckConversationAccessUseCase,
    CreateConversationWithMessageUseCase,
    GetFullUserUseCase,
    GetTopPlayersUseCase,
    GetUserGamesUseCase,
    GetUserUseCase,
    SendMessageUseCase,
)
from teamup.core.di import (
    get_announcement_repository,
    get_conversation_repository,
    get_current_user,
    get_game_repository,
    get_message_repository,
    get_response_repository,
    get_user_games_repository,
    get_user_repository,
)
from teamup.infra.database import get_async_session
from teamup.schemas import TokenData


async def get_auth_service(db: AsyncSession) -> AuthService:
    return AuthService(await get_user_repository(db))


async def get_announcement_service(db: AsyncSession) -> AnnouncementService:
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


async def get_send_message_use_case(db: AsyncSession) -> SendMessageUseCase:
    return SendMessageUseCase(await get_message_repository(db))


async def get_create_conversation_use_case(
    db: AsyncSession,
) -> CreateConversationWithMessageUseCase:
    return CreateConversationWithMessageUseCase(
        await get_conversation_repository(db),
        await get_send_message_use_case(db),
    )


async def get_top_players_use_case(game_name: str) -> GetTopPlayersUseCase:
    return GetTopPlayersUseCase(game_name)


async def get_check_conversation_access_use_case(
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> CheckConversationAccessUseCase:
    return CheckConversationAccessUseCase(db=db, user_id=token_data.user_id)
