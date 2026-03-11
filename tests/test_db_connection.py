import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.teamup.core import settings

engine = create_async_engine(
    settings.db.get_dsn(), echo=settings.application.get_debug()
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.mark.asyncio
async def test_db_connection():
    async with async_session() as session:
        res = await session.execute(text("SELECT 1"))
        assert res.scalar() is not None
