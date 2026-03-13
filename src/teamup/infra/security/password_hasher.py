```python
from passlib.context import CryptContext

class PasswordHasher:
    """
    A utility class for hashing and verifying passwords using Passlib.
    """

    _context = CryptContext(schemes=["argon2"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using the configured Passlib scheme.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return PasswordHasher._context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifies a password against a hashed password.

        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        return PasswordHasher._context.verify(password, hashed_password)
```