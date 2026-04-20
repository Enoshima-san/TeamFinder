from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from teamup.domain import IUserRepository, User

from ..database import UserMapper, UserORM


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.logger.info("Инициализация UserRepository")

    async def create(self, user: User) -> Optional[User]:
        stmt = select(UserORM).where(
            or_(UserORM.email == user.email, UserORM.username == user.username)
        )
        result = await self.session.execute(stmt)

        already_exists_user = result.scalar()
        if already_exists_user is not None:
            self.logger.warning(
                (
                    f"Пользователь с почтой {user.email} и/или "
                    f"именем пользователя{user.username} уже существует"
                )
            )
            return None
        orm = UserMapper.to_orm(user)
        try:
            self.session.add(orm)
            await self.session.flush()
            await self.session.refresh(orm)
            self.logger.info("Пользователь сохранен в сессии")
            return UserMapper.to_domain(orm)
        except IntegrityError as e:
            self.logger.error(f"Ошибка при создании пользователя: {e}")
            await self.session.rollback()
            return None

    async def delete(self, user_id: UUID) -> bool:
        orm = await self.session.get(UserORM, user_id)
        if orm is None:
            self.logger.warning(f"Пользователь с id {user_id} не найден.")
            return False

        await self.session.delete(orm)
        await self.session.flush()
        self.logger.info(f"Пользователь с id {user_id} удален из сессии.")
        return True

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = (
            select(UserORM)
            .where(UserORM.user_id == user_id)
            .options(
                selectinload(UserORM.user_games),
                selectinload(UserORM.player_rating),
                selectinload(UserORM.response),
                selectinload(UserORM.announcement),
                selectinload(UserORM.complaints),
            )
        )
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user is None:
            self.logger.warning(f"Пользователь с id {user_id} не найден")
            return None
        self.logger.info(f"Запрос на получение пользователя с ID:{user_id}")
        return UserMapper.to_domain(user)

    async def get_by_id_light(self, user_id: UUID) -> Optional[User]:
        user = await self.session.get(UserORM, user_id)
        if user is None:
            self.logger.warning(f"Пользователь с ID:{user_id} не найден")
            return None
        return UserMapper.to_domain(user)

    async def check_new_user(self, email: str, username: str) -> bool:
        stmt = select(UserORM).where(
            or_(UserORM.email == email, UserORM.username == username)
        )
        result = await self.session.execute(stmt)
        return result.scalar() is not None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user is None:
            self.logger.warning(f"Пользователь с email {email} не найден.")
            return None
        user.last_login = datetime.now()
        await self.session.flush()
        await self.session.refresh(user)
        self.logger.info(f"Запрос на получение пользователя с email {email}")
        return UserMapper.to_domain(user)

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user is None:
            self.logger.warning(f"Пользователь с username {username} не найден")
            return None
        user.last_login = datetime.now()
        await self.session.flush()
        await self.session.refresh(user)
        self.logger.info(f"Запрос на получение пользователя с username {username}")
        return UserMapper.to_domain(user)

    async def get_all(self) -> list[User]:
        stmt = select(UserORM)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        self.logger.info("Запрос на получение всех пользователей.")
        return [UserMapper.to_domain(u) for u in users]

    async def update(self, user: User) -> Optional[User]:
        orm_user = await self.session.get(UserORM, user.user_id)
        if orm_user is None:
            self.logger.warning(f"Пользователь с ID:{user.user_id} не найден")
            return None
        # Обновление сущности делается таким способом, чтобы sqlalchemy не подумала, что это новая запись
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

        await self.session.flush()
        await self.session.refresh(orm_user)
        self.logger.info(f"Пользователь с ID:{user.user_id} обновлен в сессии.")
        return UserMapper.to_domain(orm_user)
