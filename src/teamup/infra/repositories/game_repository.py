from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.domain import Game, IGameRepository

from ..database import GameMapper, GameORM


class GameRepository(IGameRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.logger.info("Инициализация GameRepository")

    async def create(self, game: Game) -> Optional[Game]:
        stmt = select(GameORM).where(
            func.lower(GameORM.game_name) == func.lower(game.game_name)
        )
        result = await self.session.execute(stmt)
        if result.scalar() is not None:
            self.logger.warning(f'Игра с именем "{game.game_name}" уже существует.')
            return None
        orm = GameMapper.to_orm(game)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        self.logger.info("Игра сохранена в сессии.")
        return GameMapper.to_domain(orm)

    async def delete(self, game_id: UUID) -> bool:
        orm = await self.session.get(GameORM, game_id)
        if orm is None:
            self.logger.warning(f"Не удалось удалить игру с ID:{game_id}.")
            return False
        await self.session.delete(orm)
        await self.session.flush()
        self.logger.info(f"Игра с ID:{game_id} удалена из сессии.")
        return True

    async def get_all(self) -> list[Game]:
        stmt = select(GameORM)
        result = await self.session.execute(stmt)
        games = result.scalars().all()
        self.logger.info("Запрос на вывод всех игра")
        return [GameMapper.to_domain(g) for g in games]

    async def get_by_id(self, game_id: UUID) -> Optional[Game]:
        game = await self.session.get(GameORM, game_id)
        if game is None:
            self.logger.warning(f"Игра c ID:{game_id} не найдена.")
            return None
        self.logger.info(f"Запрос на игру с ID:{game_id}.")
        return GameMapper.to_domain(game)

    async def get_by_name(self, game_name: str) -> Optional[Game]:
        stmt = select(GameORM).where(
            func.lower(GameORM.game_name) == func.lower(game_name)
        )
        result = await self.session.execute(stmt)
        game = result.scalar()
        if game is None:
            self.logger.warning(f'Игра "{game_name}" не найдена.')
            return None
        self.logger.info(f'Запрос на игру по имени "{game_name}" найдена.')
        return GameMapper.to_domain(game)
