from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class UserGames:
    user_id: UUID
    game_id: UUID
    preferred: bool = False

    user_game_id: UUID = field(default_factory=uuid4)

    def set_preferred(self, preferred: bool):
        """Устанавливает предпочтение пользователя для игры"""
        self.preferred = preferred
