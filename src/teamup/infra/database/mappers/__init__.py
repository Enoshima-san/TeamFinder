```python
# Import necessary mappers
from .player_rating import PlayerRatingMapper
from .user import UserMapper
from .user_games import UserGamesMapper

# Define the list of modules to be exported
__all__ = ["PlayerRatingMapper", "UserMapper", "UserGamesMapper"]
```