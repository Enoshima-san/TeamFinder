```python
from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Rank:
    """
    Represents a rank in a game.

    Attributes:
        game_id (UUID): Unique identifier of the game.
        rank_name (str): Name of the rank.
        rank_level (int): Level of the rank (e.g., MMR).
        rank_id (UUID): Unique identifier of the rank (auto-generated).
    """
    game_id: UUID
    rank_name: str
    rank_level: int  # level of the rank (e.g., MMR)
    rank_id: UUID = field(default_factory=uuid4)

    def set_rank_level(self, new_level: int) -> None:
        """
        Sets the level of the rank.

        Args:
            new_level (int): New level of the rank.

        Raises:
            ValueError: If the new level is negative.
        """
        if new_level < 0:
            raise ValueError("Rank level cannot be negative")
        self.rank_level = new_level

    def set_rank_name(self, new_name: str) -> None:
        """
        Sets the name of the rank.

        Args:
            new_name (str): New name of the rank.

        Raises:
            ValueError: If the new name is too long or too short, or contains non-alphanumeric characters.
        """
        if len(new_name) > 50:
            raise ValueError("Rank name cannot exceed 50 characters")
        if len(new_name) < 3:
            raise ValueError("Rank name must be at least 3 characters long")
        if not new_name.isalnum():
            raise ValueError("Rank name can only contain letters and numbers")
        self.rank_name = new_name

    @staticmethod
    def create(game_id: UUID, rank_name: str, rank_level: int) -> "Rank":
        """
        Creates a new rank instance.

        Args:
            game_id (UUID): Unique identifier of the game.
            rank_name (str): Name of the rank.
            rank_level (int): Level of the rank (e.g., MMR).

        Returns:
            Rank: A new rank instance.
        """
        return Rank(game_id, rank_name, rank_level)
```