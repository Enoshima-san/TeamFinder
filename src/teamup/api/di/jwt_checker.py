from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from teamup.core import get_logger, settings
from teamup.schemas import JwtPayload, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = get_logger()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Определяет текущего пользователя на основе токена.
    """
    try:
        logger.debug("Декодируем JWT.")
        payload = jwt.decode(
            token,
            settings.security.get_secret_key(),
            algorithms=[settings.security.get_algorithm()],
        )
        validate_payload = JwtPayload(**payload)

        user_data = validate_payload.sub
        if not user_data:
            logger.error("Неверный токен")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.InvalidTokenError:
        logger.error("Неверный токен.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("Токен проверен. Получаем данные пользователя.")
    return TokenData(
        user_id=UUID(validate_payload.sub),
        username=validate_payload.username,
        role=validate_payload.role,
        exp=validate_payload.exp,
    )
