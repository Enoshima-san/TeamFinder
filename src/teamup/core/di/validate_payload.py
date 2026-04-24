from uuid import UUID

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt

from teamup.core import get_logger, settings
from teamup.schemas import JwtPayload, TokenData

logger = get_logger()


def _validate_token_payload(token: str) -> TokenData:
    """
    Общая логика валидации JWT.
    Вызывается и из HTTP, и из WebSocket зависимостей.
    """
    try:
        payload = jwt.decode(
            token,
            settings.security.get_secret_key(),
            algorithms=[settings.security.get_algorithm()],
        )
        validated_payload = JwtPayload(**payload)

        if not validated_payload.sub:
            raise ValueError("Missing 'sub' in token")

        return TokenData(
            user_id=UUID(validated_payload.sub),
            email=validated_payload.email,
            username=validated_payload.username,
            role=validated_payload.role,
            exp=validated_payload.exp,
        )

    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValueError, KeyError) as e:
        logger.error(f"Token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
