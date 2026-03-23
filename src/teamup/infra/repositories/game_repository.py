from typing import Optional
from uuid import UUID

from sqlalchemy import func, select

from src.teamup.core import get_logger
from src.teamup.domain import Game, IGameRepository

from ..database import GameMapper, GameORM, async_session

logger = get_logger()


class GameRepository(IGameRepository):
    def __init__(self):
        super().__init__()
        logger.info("GameRepository проиницилизирован")

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create(self, game: Game) -> Optional[Game]:
        self.check_session()
        stmt = select(GameORM).where(
            func.lower(GameORM.game_name) == func.lower(game.game_name)
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        if result.scalar() is not None:
            logger.warning(f'Игра с именем "{game.game_name}" уже существует.')
            return None

        orm = GameMapper.to_orm(game)
        self.session.add(orm)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]

        logger.info(f'В сущность Game добавлена игры "{game.game_name}".')
        return GameMapper.to_domain(orm)

    async def delete(self, game: Game) -> bool:
        self.check_session()
        orm = await self.session.get(GameORM, game.game_id)  # type: ignore[reportOptionalMemberAccess]
        if orm is None:
            logger.warning(
                f'Не удалось удалить игру "{game.game_name}" в сущности Game.'
            )
            return False

        await self.session.delete(orm)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]

        logger.info(f"Из сущности Game удалена запись - {game.game_name}.")
        return True

    async def get_all(self) -> list[Game]:
        self.check_session()
        stmt = select(GameORM)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        games = result.scalars().all()

        return [GameMapper.to_domain(g) for g in games]

    async def get_by_id(self, game_id: UUID) -> Optional[Game]:
        self.check_session()
        game = await self.session.get(GameORM, game_id)  # type: ignore[reportOptionalMemberAccess]
        if game is None:
            logger.warning(f"Игра c ID:{game_id} в сущности c Game не найдена.")
            return None

        logger.info(f"Игра с ID:{game_id} Game найдена.")
        return GameMapper.to_domain(game)

    async def get_by_name(self, game_name: str) -> Optional[Game]:
        self.check_session()
        stmt = select(GameORM).where(
            func.lower(GameORM.game_name) == func.lower(game_name)
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        game = result.scalar()

        if game is None:
            logger.warning(f'Игра "{game_name}" в сущности Game не найдена.')
            return None

        logger.info(f'Игра "{game_name}" в сущности Game найдена.')
        return GameMapper.to_domain(game)
