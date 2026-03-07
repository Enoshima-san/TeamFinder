from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class UserGames:
    user_id: UUID
    game_id: UUID
    user_game_id: UUID = field(default_factory=uuid4)

    preferred: bool = False

    def set_preferred(self, preferred: bool):
        """Устанавливает предпочтение пользователя для игры"""
        self.preferred = preferred
