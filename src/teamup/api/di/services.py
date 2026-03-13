```python
from src.teamup.application import IAuthService
from src.teamup.infra import AuthService
from .repositories import get_user_repository

async def get_auth_service() -> IAuthService:
    """
    Retrieves an instance of AuthService, injecting the user repository.

    Returns:
        IAuthService: An instance of AuthService with the user repository injected.
    """
    return AuthService(await get_user_repository())
```