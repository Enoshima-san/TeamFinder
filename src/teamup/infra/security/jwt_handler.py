from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import jwt

from teamup.core import settings


class JWTHandler:
    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (
            expires_delta
            or timedelta(minutes=settings.security.get_access_token_expires())
        )
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(
            to_encode,
            settings.security.get_secret_key(),
            algorithm=settings.security.get_algorithm(),
        )

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(
            days=settings.security.get_refresh_token_expires()
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(
            to_encode,
            settings.security.get_secret_key(),
            algorithm=settings.security.get_algorithm(),
        )

    @staticmethod
    def verify_token(token: str, token_type: str) -> dict | None:
        payload = JWTHandler.decode_token(token)
        if payload and payload.get("type") == token_type:
            return payload
        return None

    @staticmethod
    def decode_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                settings.security.get_secret_key(),
                algorithms=[settings.security.get_algorithm()],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_token_data(
        user_id: UUID, username: str, email: str, role: str
    ) -> dict[str, str]:
        """Формирует `payload` - содержимое JWT"""
        return {"sub": str(user_id), "email": email, "username": username, "role": role}
