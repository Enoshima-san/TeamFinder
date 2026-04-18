from datetime import datetime
from typing import cast
from uuid import UUID

from teamup.domain import User

from ..models import UserORM
from ._map_relation import _map_relation
from .announcement import AnnouncementMapper
from .complaints import ComplaintsMapper
from .conversation import ConversationMapper
from .notification import NotificationMapper
from .player_rating import PlayerRatingMapper
from .response import ResponseMapper
from .user_games import UserGamesMapper


class UserMapper:
    @staticmethod
    def to_domain(orm: UserORM | None) -> User:
        if not orm:
            raise ValueError("ORM object is None")

        user_games = _map_relation(orm, "user_games", UserGamesMapper.to_domain)
        user_rating = _map_relation(orm, "player_rating", PlayerRatingMapper.to_domain)
        user_response = _map_relation(orm, "user_response", ResponseMapper.to_domain)
        user_announcement = _map_relation(
            orm, "announcement", AnnouncementMapper.to_domain
        )
        user_complaints = _map_relation(orm, "complaints", ComplaintsMapper.to_domain)
        user_conversations = _map_relation(
            orm, "authored_conversations", ConversationMapper.to_domain
        ) + _map_relation(orm, "responded_conversations", ConversationMapper.to_domain)
        user_notifications = _map_relation(
            orm, "notifications", NotificationMapper.to_domain
        )

        return User(
            user_id=cast(UUID, orm.user_id),
            username=orm.username,
            email=orm.email,
            password_hash=orm.password_hash,
            age=orm.age,
            about_me=orm.about_me,
            blocked_reason=orm.blocked_reason,
            registration_date=orm.registration_date,
            last_login=orm.last_login,
            is_active=orm.is_active,
            role=orm.role,
            is_blocked=orm.is_blocked,
            user_games=user_games,
            user_rating=user_rating,
            user_response=user_response,
            user_announcement=user_announcement,
            user_complaints=user_complaints,
            user_conversations=sorted(
                user_conversations,
                key=lambda obj: obj.last_message_at or datetime.min,
                reverse=True,
            ),
            user_notifications=user_notifications,
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
        )
