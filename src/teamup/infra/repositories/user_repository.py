from typing import Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.teamup.core import get_logger
from src.teamup.domain import IUserRepository, User

from ..database import UserMapper, UserORM, async_session

logger = get_logger()


class UserRepository(IUserRepository):
    def __init__(self):
        super().__init__()
        logger.info("UserRepository проиницилизирован")

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create(self, user: User) -> Optional[User]:
        self.check_session()
        stmt = select(UserORM).where(
            or_(UserORM.email == user.email, UserORM.username == user.username)
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]

        already_exists_user = result.scalar()
        if already_exists_user is not None:
            logger.warning(
                (
                    f"Пользователь с почтой {user.email} и/или "
                    f"именем пользователя{user.username} уже существует"
                )
            )
            return None

        orm = UserMapper.to_orm(user)

        try:
            self.session.add(orm)  # type: ignore[reportOptionalMemberAccess]
            await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
            await self.session.refresh(orm)  # type: ignore[reportOptionalMemberAccess]
            logger.info(f"Пользователь с id {user.user_id} создан")
            return UserMapper.to_domain(orm)
        except IntegrityError:
            logger.error(f"Ошибка при создании пользователя с id {user.user_id}")
            await self.session.rollback()  # type: ignore[reportOptionalMemberAccess]
            return None

    async def delete(self, user: User) -> bool:
        self.check_session()
        orm = await self.session.get(UserORM, user.user_id)  # type: ignore[reportOptionalMemberAccess]
        if orm is None:
            logger.warning(f"Пользователь с id {user.user_id} не найден")
            return False

        await self.session.delete(orm)  # type: ignore[reportOptionalMemberAccess]
        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        logger.info(f"Пользователь с id {user.user_id} удален")
        return True

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        self.check_session()
        stmt = select(UserORM).options(
            selectinload(UserORM.user_games),
            selectinload(UserORM.player_rating),
            selectinload(UserORM.response),
            selectinload(UserORM.announcement),
            selectinload(UserORM.complaints),
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        user = result.scalar()

        if user is None:
            logger.warning(f"Пользователь с id {user_id} не найден")
            return None

        return UserMapper.to_domain(user)

    async def check_new_user(self, email: str, username: str) -> bool:
        self.check_session()
        stmt = select(UserORM).where(
            or_(UserORM.email == email, UserORM.username == username)
        )
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]

        return result.scalar() is not None

    async def get_by_email(self, email: str) -> Optional[User]:
        self.check_session()
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        user = result.scalar()

        if user is None:
            logger.warning(f"Пользователь с email {email} не найден")
            return None

        return UserMapper.to_domain(user)

    async def get_by_username(self, username: str) -> Optional[User]:
        self.check_session()
        stmt = select(UserORM).where(UserORM.username == username)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        user = result.scalar()

        if user is None:
            logger.warning(f"Пользователь с username {username} не найден")
            return None

        return UserMapper.to_domain(user)

    async def get_all(self) -> list[User]:
        self.check_session()
        stmt = select(UserORM)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        users = result.scalars().all()

        return [UserMapper.to_domain(u) for u in users]

    async def update(self, user: User) -> Optional[User]:
        self.check_session()
        stmt = select(UserORM).where(UserORM.user_id == user.user_id)
        result = await self.session.execute(stmt)  # type: ignore[reportOptionalMemberAccess]
        orm_user = result.scalar()

        if orm_user is None:
            logger.warning(f"Пользователь с id {user.user_id} не найден")
            return None

        orm_user.username = user.username
        orm_user.password_hash = user.password_hash
        orm_user.last_login = user.last_login
        orm_user.is_active = user.is_active
        orm_user.role = user.role
        orm_user.has_microphone = user.has_microphone
        orm_user.age = user.age
        orm_user.about_me = user.about_me
        orm_user.is_blocked = user.is_blocked
        orm_user.blocked_reason = user.blocked_reason

        await self.session.commit()  # type: ignore[reportOptionalMemberAccess]
        await self.session.refresh(orm_user)  # type: ignore[reportOptionalMemberAccess]

        return UserMapper.to_domain(orm_user)
