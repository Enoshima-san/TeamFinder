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
        super().__init__()
        logger.info("UserGamesRepository проиницилизирован")

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create(self, user_game: UserGames) -> Optional[UserGames]:
        self.check_session()
        orm = UserGamesMapper.to_orm(user_game)
        self.session.add(orm)  # type: ignore[reportOptionalMemberAccess]

        try:
            await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
            await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]
            return UserGamesMapper.to_domain(orm)
        except IntegrityError as e:
            await self.session.rollback()  # type: ignore[reportOptionalMemberAccess]
            logger.warning(
                f"Не удалось добавить игру {user_game.game_id} для пользователя {user_game.user_id}. Ошибка: {e._message}."
            )
            return None

    async def remove(self, user_id: UUID, game_id: UUID) -> bool:
        self.check_session()
        stmt = select(UserGamesORM).where(
            UserGamesORM.user_id == user_id, UserGamesORM.game_id == game_id
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        orm = result.scalar()

        if orm is None:
            logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return False

        await self.session.delete(orm)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]

        return True

    async def get(self, user_id: UUID, game_id: UUID) -> Optional[UserGames]:
        self.check_session()
        stmt = (
            select(UserGamesORM)
            .where(UserGamesORM.user_id == user_id)
            .where(UserGamesORM.game_id == game_id)
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        user_game = result.scalar()

        if user_game is None:
            logger.warning(f"Связь не найдена: user={user_id} <=> game={game_id}")
            return None
        return UserGamesMapper.to_domain(user_game)

    async def get_all(self, user_id: UUID) -> list[UserGames]:
        self.check_session()
        stmt = select(UserGamesORM)
        results = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        user_games = results.scalars().all()

        return [UserGamesMapper.to_domain(ug) for ug in user_games]
