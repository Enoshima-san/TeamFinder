from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from teamup.core import get_logger
from teamup.schemas import TokenData

from .validate_payload import _validate_token_payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = get_logger()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """HTTP-версия: токен из заголовка Authorization: Bearer ..."""
    try:
        return _validate_token_payload(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
