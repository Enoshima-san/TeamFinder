import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text

from ...core import logger, settings

engine = create_async_engine(
    settings.db.get_dsn(), echo=settings.application.get_debug()
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def check_database_connection(max_retries=10, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            async with async_session() as session:
                await session.execute(text("SELECT 1"))
            logger.info(f"Подключение к базе данных удалось на {attempt} попытке")
            return
        except OperationalError as e:
            if attempt == max_retries:
                raise e
            logger.warning(
                f"База данных не готова ({attempt}/{max_retries} попыток), начинаем заново через {delay}сек..."
            )
            await asyncio.sleep(delay)
