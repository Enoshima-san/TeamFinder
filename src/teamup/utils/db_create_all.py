import asyncio

from src.teamup.core import logger
from src.teamup.infra import Base, engine


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Все таблицы созданы!")


def run_create_all():
    asyncio.run(create_database())


if __name__ == "__main__":
    run_create_all()
