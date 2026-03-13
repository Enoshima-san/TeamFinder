from typing import Any, Callable, TypeVar, cast

from sqlalchemy.inspection import inspect

from src.teamup.domain import User

from ..models import UserORM
from .announcement import AnnouncementMapper
from .complaints import ComplaintsMapper
from .player_rating import PlayerRatingMapper
from .response import ResponseMapper
from .user_games import UserGamesMapper

T = TypeVar("T")


def _safe_map_relation(
    orm: Any, relation_name: str, mapper: Callable[[Any], T]
) -> list[T]:
    """
    Безопасно маппит отношение: если не загружено — возвращает пустой список.
    """
    try:
        # Проверяем, загружено ли отношение через SQLAlchemy inspection API
        insp = inspect(orm)
        if relation_name in insp.unloaded:
            return []

        data = getattr(orm, relation_name)
        return [mapper(item) for item in (data or [])]
    except Exception:
        # Любая ошибка (например, доступ к незагруженному отношению) → пустой список
        return []


class UserMapper:
    @staticmethod
    def to_domain(orm: UserORM | None) -> User:
        if not orm:
            raise ValueError("ORM object is None")

        user_games = _safe_map_relation(orm, "user_games", UserGamesMapper.to_domain)
        user_ratings = _safe_map_relation(
            orm, "player_rating", PlayerRatingMapper.to_domain
        )
        user_responses = _safe_map_relation(orm, "response", ResponseMapper.to_domain)
        user_announcements = _safe_map_relation(
            orm, "announcement", AnnouncementMapper.to_domain
        )
        user_complaints = _safe_map_relation(
            orm, "complaints", ComplaintsMapper.to_domain
        )

        return User(
            user_id=cast(Any, orm.user_id),
            username=cast(Any, orm.username),
            email=cast(Any, orm.email),
            password_hash=cast(Any, orm.password_hash),
            age=cast(Any, orm.age),
            about_me=cast(Any, orm.about_me),
            blocked_reason=cast(Any, orm.blocked_reason),
            registration_date=cast(Any, orm.registration_date),
            last_login=cast(Any, orm.last_login),
            is_active=cast(Any, orm.is_active),
            role=cast(Any, orm.role),
            is_blocked=cast(Any, orm.is_blocked),
            user_games=user_games,
            user_ratings=user_ratings,
            user_responses=user_responses,
            user_announcements=user_announcements,
            user_complaints=user_complaints,
        )

    @staticmethod
    def to_orm(entity: User | None) -> UserORM:
        if not entity:
            raise ValueError("Entity is None")

        return UserORM(
            user_id=entity.user_id,
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash,
            age=entity.age,
            about_me=entity.about_me,
            blocked_reason=entity.blocked_reason,
            registration_date=entity.registration_date,
            last_login=entity.last_login,
            is_active=entity.is_active,
            role=entity.role,
            is_blocked=entity.is_blocked,
            # ← Отношения не маппим здесь — они управляются через session.add()/relationships
        )
