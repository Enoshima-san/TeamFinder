import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..enums import UserRole
from .announcement import Announcement
from .complaints import Complaints
from .player_rating import PlayerRating
from .response import Response
from .user_games import UserGames


@dataclass
class User:
    email: str
    username: str
    password_hash: str
    user_id: UUID = field(default_factory=uuid4)

    registration_date: datetime = field(default_factory=datetime.now)
    last_login: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    role: str = UserRole.USER.value
    has_microphone: bool = False
    age: Optional[int] = None
    about_me: Optional[str] = None
    is_blocked: bool = False
    blocked_reason: Optional[str] = None

    user_games: List["UserGames"] = field(default_factory=list)
    user_rating: List["PlayerRating"] = field(default_factory=list)
    user_response: List["Response"] = field(default_factory=list)
    user_announcement: List["Announcement"] = field(default_factory=list)
    user_complaints: List["Complaints"] = field(default_factory=list)

    def set_username(self, username: str):
        """Установка имени пользователя"""
        if len(username) == 0:
            raise ValueError("Имя пользователя не может быть пустым")
        if len(username) < 3:
            raise ValueError("Имя пользователя слишком короткое")
        if len(username) > 15:
            raise ValueError("Имя пользователя слишком длинное")
        self.username = username

    def set_about(self, about: str):
        """Установка описания пользователя"""
        if len(about) > 255:
            raise ValueError("Описание пользователя слишком длинное")
        self.about = about

    def go_online(self):
        """Пользователь онлайн"""
        self.is_active = True

    def go_offline(self):
        """Пользователь оффлайн"""
        self.is_active = False

    def block(self, reason: str):
        """Блокировка пользователя"""
        if self.is_blocked:
            raise ValueError("Пользователь уже заблокирован")
        if not reason:
            raise ValueError("Причина блокировки обязательна")

        self.is_blocked = True
        self.blocked_reason = reason

    def unblock(self):
        """Разблокировка"""
        if not self.is_blocked:
            raise ValueError("Пользователь не заблокирован")

        self.is_blocked = False
        self.blocked_reason = None

    def is_admin(self) -> bool:
        """Проверка роли"""
        return self.role == UserRole.ADMIN.value

    def add_game(self, game_id: UUID) -> "UserGames":
        """Добавление игры с проверкой на дубликат"""
        if any(ug.game_id == game_id for ug in self.user_games):
            raise ValueError("Игра уже добавлена пользователю")

        user_game = UserGames(user_id=self.user_id, game_id=game_id)
        self.user_games.append(user_game)
        return user_game

    def remove_game(self, game_id: UUID):
        """Удаление игры"""
        self.user_games = [ug for ug in self.user_games if ug.game_id != game_id]

    @staticmethod
    def create(
        email: str,
        username: str,
        password_hash: str,
        age: Optional[int] = None,
        role: str = UserRole.USER.value,
        about_me: Optional[str] = None,
        blocked_reason: Optional[str] = None,
        registration_date: datetime = datetime.now(),
        last_login: datetime = datetime.now(),
        is_active: bool = True,
        is_blocked: bool = False,
    ) -> "User":
        if (
            not email
            or "@"
            or len(email) > 255
            or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        ):
            raise ValueError("Некорректный email")
        if len(username) < 3:
            raise ValueError("Имя пользователя слишком короткое")
        if len(username) > 15:
            raise ValueError("Имя пользователя слишком длинное")

        return User(
            email=email,
            username=username,
            password_hash=password_hash,
            age=age,
            role=role,
            about_me=about_me,
            is_active=is_active,
            is_blocked=is_blocked,
            blocked_reason=blocked_reason,
            registration_date=registration_date,
            last_login=last_login,
        )
