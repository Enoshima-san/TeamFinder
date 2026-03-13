from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Rank:
    game_id: UUID
    rank_name: str
    rank_level: int  # полагаю кол-во ММР
    rank_id: UUID = field(default_factory=uuid4)

    def set_rank_level(self, new_level: int):
        """Устанавливает уровень ранга"""
        if new_level < 0:
            raise ValueError("Уровень ранга не может быть отрицательным")
        self.rank_level = new_level

    def set_rank_name(self, new_name: str):
        """Устанавливает наименование ранга"""
        if len(new_name) > 50:
            raise ValueError("Наименовние ранга не может превышать 50 символов")
        if len(new_name) < 3:
            raise ValueError("Наименовние ранга не может быть меньше 3 символов")
        if not new_name.isalnum():
            raise ValueError("Наименовние ранга может содержать только буквы и цифры")
        self.rank_name = new_name

    @staticmethod
    def create(game_id: UUID, rank_name: str, rank_level: int) -> "Rank":
        return Rank(game_id, rank_name, rank_level)
