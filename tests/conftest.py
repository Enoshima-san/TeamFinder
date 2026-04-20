import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from teamup.core import settings


@pytest.fixture(scope="session")
def event_loop():
    """Создаём event loop для asyncio-тестов."""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Фикстура для предоставления чистой AsyncSession на каждый тест.
    Использует тестовую БД или in-memory SQLite для изоляции.
    """
    engine = create_async_engine(
        settings.db.get_dsn(),
        echo=False,
    )

    testing_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with testing_session_maker() as session:
        try:
            yield session
            await session.commit()  # коммитим, если тест прошёл
        except Exception:
            await session.rollback()  # откатываем при ошибке теста
            raise
        finally:
            await session.close()
            await engine.dispose()  # освобождаем соединения
