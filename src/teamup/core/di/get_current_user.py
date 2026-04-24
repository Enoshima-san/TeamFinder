from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from teamup.core import get_logger
from teamup.schemas import TokenData

from .validate_payload import _validate_token_payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = get_logger()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """HTTP-версия: токен из заголовка Authorization: Bearer ..."""
    return _validate_token_payload(token)
