from uuid import UUID

from fastapi import Query, WebSocket, WebSocketException, status
from jose import JWTError, jwt

from teamup.core import get_logger, settings
from teamup.schemas import JwtPayload, TokenData

logger = get_logger()


async def get_current_user_ws(
    websocket: WebSocket,
    token: str | None = Query(None),
) -> TokenData:
    if token is None:
        token = websocket.query_params.get("token")

    if not token:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token"
        )

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

    except (JWTError, ValueError, KeyError) as e:
        logger.error(f"Token validation failed: {e}")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired token"
        )
