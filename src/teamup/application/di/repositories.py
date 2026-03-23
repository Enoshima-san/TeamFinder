from src.teamup.domain import (
    IAnnouncementRepository,
    IGameRepository,
    IUserGamesRepository,
    IUserRepository,
)
from src.teamup.infra import (
    AnnouncementRepository,
    GameRepository,
    UserGamesRepository,
    UserRepository,
)


async def get_user_repository() -> IUserRepository:
    return UserRepository()


async def get_game_repository() -> IGameRepository:
    return GameRepository()


async def get_user_games_repository() -> IUserGamesRepository:
    return UserGamesRepository()


async def get_announcement_repository() -> IAnnouncementRepository:
    return AnnouncementRepository()
