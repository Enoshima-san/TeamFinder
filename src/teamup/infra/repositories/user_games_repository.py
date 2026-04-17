from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core import get_logger
from teamup.domain import IUserGamesRepository, UserGames

from ..database import UserGamesMapper, UserGamesORM


class UserGamesRepository(IUserGamesRepository):
    def __init__(self, session: AsyncSession):
        self.logger = get_logger()
        self.session = session
        self.logger.info("Инициализация UserGamesRepository")

    async def create(self, user_game: UserGames) -> Optional[UserGames]:
        orm = UserGamesMapper.to_orm(user_game)
        self.session.add(orm)
        try:
            await self.session.flush()
            await self.session.refresh(orm)
            self.logger.info("Игра пользователя сохранена в сессии.")
            return UserGamesMapper.to_domain(orm)
        except IntegrityError as e:
            await self.session.rollback()
            self.logger.warning(
                f"Не удалось добавить игру {user_game.game_id} для пользователя {user_game.user_id}. Ошибка: {e._message}."
            )
            return None

    async def delete(self, user_id: UUID, game_id: UUID) -> bool:
        stmt = select(UserGamesORM).where(
            UserGamesORM.user_id == user_id, UserGamesORM.game_id == game_id
        )
        result = await self.session.execute(stmt)
        orm = result.scalar()
        if orm is None:
            self.logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return False
        await self.session.delete(orm)
        await self.session.flush()
        self.logger.info(
            f"Игра {game_id}  для пользователя {user_id} удалена из сессии."
        )
        return True

    async def get_by_fk(self, user_id: UUID, game_id: UUID) -> Optional[UserGames]:
        stmt = (
            select(UserGamesORM)
            .where(UserGamesORM.user_id == user_id)
            .where(UserGamesORM.game_id == game_id)
        )
        result = await self.session.execute(stmt)
        user_game = result.scalar()
        if user_game is None:
            self.logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return None
        self.logger.info(f"Запрос на получение связи user={user_id} <=> game={game_id}")
        return UserGamesMapper.to_domain(user_game)

    async def get_all_by_user(self, user_id: UUID) -> list[UserGames]:
        stmt = select(UserGamesORM).where(UserGamesORM.user_id == user_id)
        results = await self.session.execute(stmt)
        user_games = results.scalars().all()
        self.logger.info(
            f"Запрос на получение всех игр для пользователя с ID:{user_id}."
        )
        return [UserGamesMapper.to_domain(ug) for ug in user_games]
