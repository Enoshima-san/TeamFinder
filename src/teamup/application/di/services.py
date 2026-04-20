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
    GetConversationsByUserIdUseCase,
    GetConversationWithMessagesUseCase,
    GetFullUserUseCase,
    GetTopPlayersUseCase,
    GetUserGamesUseCase,
    GetUserUseCase,
    SendMessageUseCase,
    UpdateUserUseCase,
)
from teamup.core.di import (
    get_announcement_repository,
    get_conversation_repository,
    get_current_user,
    get_current_user_ws,
    get_game_repository,
    get_message_repository,
    get_response_repository,
    get_user_games_repository,
    get_user_repository,
)
from teamup.domain import (
    IAnnouncementRepository,
    IConversationRepository,
    IMessageRepository,
    IUserRepository,
)
from teamup.infra.database import get_async_session
from teamup.schemas import TokenData


async def get_auth_service(
    db: AsyncSession = Depends(get_async_session),
) -> AuthService:
    return AuthService(await get_user_repository(db))


async def get_announcement_service(
    db: AsyncSession = Depends(get_async_session),
) -> AnnouncementService:
    return AnnouncementService(
        await get_announcement_repository(db),
        await get_user_repository(db),
        await get_game_repository(db),
    )


async def get_responses_service(
    db: AsyncSession = Depends(get_async_session),
) -> ResponsesService:
    return ResponsesService(
        await get_response_repository(db),
        await get_user_repository(db),
        await get_announcement_repository(db),
    )


async def get_games_service(
    db: AsyncSession = Depends(get_async_session),
) -> GamesService:
    return GamesService(await get_game_repository(db))


async def get_add_game_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> AddGameUseCase:
    return AddGameUseCase(
        await get_user_games_repository(db),
        await get_user_repository(db),
        await get_game_repository(db),
    )


async def get_full_user_info_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> GetFullUserUseCase:
    return GetFullUserUseCase(await get_user_repository(db))


async def get_user_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> GetUserUseCase:
    return GetUserUseCase(await get_user_repository(db))


async def get_user_games_use_case(
    db: AsyncSession = Depends(get_async_session),
) -> GetUserGamesUseCase:
    return GetUserGamesUseCase(
        await get_user_games_repository(db), await get_game_repository(db)
    )


async def get_send_message_use_case(
    mess_r: IMessageRepository = Depends(get_message_repository),
) -> SendMessageUseCase:
    return SendMessageUseCase(mess_r)


async def get_create_conversation_use_case(
    conv_r: IConversationRepository = Depends(get_conversation_repository),
    sm_uc: SendMessageUseCase = Depends(get_send_message_use_case),
) -> CreateConversationWithMessageUseCase:
    return CreateConversationWithMessageUseCase(
        conv_r=conv_r,
        sm_us=sm_uc,
    )


async def get_top_players_use_case(game_name: str) -> GetTopPlayersUseCase:
    return GetTopPlayersUseCase(game_name)


async def get_check_conversation_access_use_case(
    ann_r: IAnnouncementRepository = Depends(get_announcement_repository),
    user_r: IUserRepository = Depends(get_user_repository),
    conv_r: IConversationRepository = Depends(get_conversation_repository),
) -> CheckConversationAccessUseCase:
    return CheckConversationAccessUseCase(
        ann_r=ann_r,
        user_r=user_r,
        conv_r=conv_r,
    )


async def get_conversation_with_messages_use_case(
    mess_r: IMessageRepository = Depends(get_message_repository),
    user_r: IUserRepository = Depends(get_user_repository),
    conv_r: IConversationRepository = Depends(get_conversation_repository),
) -> GetConversationWithMessagesUseCase:
    return GetConversationWithMessagesUseCase(
        mess_r=mess_r,
        user_r=user_r,
        conv_r=conv_r,
    )


async def get_conversation_by_user_id_use_case(
    conv_r: IConversationRepository = Depends(get_conversation_repository),
    user_r: IUserRepository = Depends(get_user_repository),
) -> GetConversationsByUserIdUseCase:
    return GetConversationsByUserIdUseCase(conv_r=conv_r, user_r=user_r)


async def get_update_user_use_case(
    user_r: IUserRepository = Depends(get_user_repository),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_r=user_r)
