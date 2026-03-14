from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from src.teamup.application import IUserRepository
from src.teamup.core import logger
from src.teamup.domain import User

from ..database import UserMapper, UserORM, async_session


class UserRepository(IUserRepository):
    def __init__(self):
        self.session = async_session()
        logger.info("UserRepository проинициализирован")

    async def create(self, user: User) -> User | None:
        """
        Возвращает User\n\n
        Если пользователь уже в базе, возваращает `None`,
        иначе возвращаем пустого пользователся
        """
        stmt = select(UserORM).where(
            UserORM.email == user.email and UserORM.username == user.username
        )
        result = await self.session.execute(stmt)

        already_exists_user = result.scalar()
        if already_exists_user:
            logger.warning(
                (
                    f"Пользователь с почтой {user.email} и/или "
                    f"именем пользователя{user.username} уже существует"
                )
            )
            return None

        orm = UserMapper.to_orm(user)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        logger.info(f"Пользователь с id {user.user_id} создан")

        return UserMapper.to_domain(orm)

    async def delete(self, user: int | User) -> bool:
        """Возвращает результат удаения пользователя"""
        if isinstance(user, int):
            orm_user = await self.session.get(UserORM, user)
            if not orm_user:
                logger.warning(f"Пользователь с id {user} не найден")
                return False
            await self.session.delete(orm_user)
            await self.session.commit()
            logger.info(f"Пользователь с id {user} удален")
            return True

        orm_user = await self.session.get(UserORM, user.user_id)
        if not orm_user:
            logger.warning(f"Пользователь с id {user.user_id} не найден")
            return False
        await self.session.delete(orm_user)
        await self.session.commit()
        logger.info(f"Пользователь с id {user.user_id} удален")
        return True

    async def get_by_id(self, id: UUID) -> User | None:
        """
        Возвращает User\n\n
        Если пользователь не найден, возваращает `None`
        """
        stmt = select(UserORM).options(
            selectinload(UserORM.user_games),
            selectinload(UserORM.player_rating),
            selectinload(UserORM.response),
            selectinload(UserORM.announcement),
            selectinload(UserORM.complaints),
        )
        result = await self.session.execute(stmt)
        user = result.scalar()

        if not user:
            logger.warning(f"Пользователь с id {id} не найден")
            return None

        return UserMapper.to_domain(user)

    async def check_new_user(self, email: str, username: str) -> bool:
        """
        Проверяет, существует ли пользователь с указанным email и username\n\n
        Возвращает `True`, если пользователь не найден, иначе `False`
        """
        stmt = select(UserORM).where(
            or_(UserORM.email == email, UserORM.username == username)
        )
        result = await self.session.execute(stmt)

        return result.scalar() is not None

    async def get_by_email(self, email: str) -> User | None:
        """
        Возвращает User\n\n
        Если пользователь не найден, возваращает `None`
        """
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar()

        if not user:
            logger.warning(f"Пользователь с email {email} не найден")
            return None

        return UserMapper.to_domain(user)

    async def get_by_username(self, username: str) -> User | None:
        """
        Возвращает User\n\n
        Если пользователь не найден, возваращает `None`
        """
        stmt = select(UserORM).where(UserORM.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar()

        if not user:
            logger.warning(f"Пользователь с username {username} не найден")
            return None

        return UserMapper.to_domain(user)

    async def get_all(self) -> list[User]:
        """
        Возвращает User\n\n
        Если пользователь не найден, возваращает `None`
        """
        stmt = select(UserORM)
        result = await self.session.execute(stmt)
        users = result.scalars().all()

        return [UserMapper.to_domain(user) for user in users]

    async def update(self, user: User) -> User | None:
        """
        Обновляет пользователя в базе данных\n\n
        Если пользователь не найден, возваращает `None`
        """
        stmt = select(UserORM).where(UserORM.user_id == user.user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalar()

        if not orm_user:
            logger.warning(f"Пользователь с id {user.user_id} не найден")
            return None

        orm_user.username = user.username
        orm_user.email = user.email
        orm_user.password_hash = user.password_hash
        orm_user.registration_date = user.registration_date
        orm_user.last_login = user.last_login
        orm_user.is_active = user.is_active
        orm_user.role = user.role
        orm_user.has_microphone = user.has_microphone
        orm_user.age = user.age
        orm_user.about_me = user.about_me
        orm_user.is_blocked = user.is_blocked
        orm_user.blocked_reason = user.blocked_reason

        await self.session.commit()
        await self.session.refresh(orm_user)

        return UserMapper.to_domain(orm_user)
