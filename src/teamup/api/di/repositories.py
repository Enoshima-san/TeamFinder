```python
from ...application import IUserRepository
from ...infra import UserRepository

async def get_user_repository() -> IUserRepository:
    """
    Retrieves an instance of the user repository.

    Returns:
        IUserRepository: An instance of the user repository.
    """
    # Return an instance of the user repository
    return UserRepository()
```