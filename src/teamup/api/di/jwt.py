import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ...core import settings
from ...schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Определяет текущего пользователя на основе токена.
    """
    try:
        payload = jwt.decode(
            token,
            settings.security.get_secret_key,
            algorithms=[settings.security.get_algorithm()],
        )
        user_data = payload.get("sub")
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenData(
        user_id=payload["sub"], username=payload["username"], role=payload["role"]
    )
