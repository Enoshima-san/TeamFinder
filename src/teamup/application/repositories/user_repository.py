```python
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from ...domain import User

class IUserRepository(ABC):
    """
    Abstract base class for user repositories.
    
    Provides a contract for user data storage and retrieval.
    """

    @abstractmethod
    async def create_user(self, user: User) -> Optional[User]:
        """
        Creates a new user in the repository.
        
        Args:
            user: The user to create.
        
        Returns:
            The created user, or None if creation failed.
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: int | User) -> bool:
        """
        Deletes a user from the repository.
        
        Args:
            user_id: The ID of the user to delete, or the user object itself.
        
        Returns:
            True if deletion was successful, False otherwise.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Retrieves a user by their unique ID.
        
        Args:
            user_id: The ID of the user to retrieve.
        
        Returns:
            The user object, or None if not found.
        """
        pass

    @abstractmethod
    async def check_new_user(self, email: str, username: str) -> bool:
        """
        Checks if a user with the given email and username already exists.
        
        Args:
            email: The email address to check.
            username: The username to check.
        
        Returns:
            True if a user with the given email and username already exists, False otherwise.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.
        
        Args:
            email: The email address of the user to retrieve.
        
        Returns:
            The user object, or None if not found.
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieves a user by their username.
        
        Args:
            username: The username of the user to retrieve.
        
        Returns:
            The user object, or None if not found.
        """
        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """
        Retrieves all users in the repository.
        
        Returns:
            A list of user objects.
        """
        pass

    @abstractmethod
    async def update_user(self, user: User) -> Optional[User]:
        """
        Updates an existing user in the repository.
        
        Args:
            user: The user to update.
        
        Returns:
            The updated user, or None if update failed.
        """
        pass
```