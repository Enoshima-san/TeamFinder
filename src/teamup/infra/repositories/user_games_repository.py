from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.teamup.core import get_logger
from src.teamup.domain import IUserGamesRepository, UserGames

from ..database import UserGamesMapper, UserGamesORM, async_session

logger = get_logger()


class UserGamesRepository(IUserGamesRepository):
    def __init__(self):
        logger.info("UserGamesRepository проинициализирован")
        self.session = async_session()

    async def add(self, user_game: UserGames) -> Optional[UserGames]:
        orm = UserGamesMapper.to_orm(user_game)
        self.session.add(orm)

        try:
            await self.session.commit()
            await self.session.refresh(orm)
            return UserGamesMapper.to_domain(orm)
        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                f"Не удалось добавить игру {user_game.game_id} для пользователя {user_game.user_id}. Ошибка: {e._message}."
            )
            return None

    async def remove(self, user_id: UUID, game_id: UUID) -> bool:
        stmt = select(UserGamesORM).where(
            UserGamesORM.user_id == user_id, UserGamesORM.game_id == game_id
        )
        result = await self.session.execute(stmt)
        orm = result.scalar()

        if orm is None:
            logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return False

        await self.session.delete(orm)
        await self.session.commit()

        return True

    async def get(self, user_id: UUID, game_id: UUID) -> Optional[UserGames]:
        stmt = (
            select(UserGamesORM)
            .where(UserGamesORM.user_id == user_id)
            .where(UserGamesORM.game_id == game_id)
        )
        result = await self.session.execute(stmt)
        user_game = result.scalar()

        if user_game is None:
            logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return None
        return UserGamesMapper.to_domain(user_game)

    async def get_all(self, user_id: UUID) -> list[UserGames]:
        stmt = select(UserGamesORM)
        results = await self.session.execute(stmt)
        user_games = results.scalars().all()

        return [UserGamesMapper.to_domain(ug) for ug in user_games]
