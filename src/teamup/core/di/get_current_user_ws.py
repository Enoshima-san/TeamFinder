from typing import Optional

from fastapi import Query, WebSocket, WebSocketException, status

from teamup.schemas import TokenData

from .validate_payload import _validate_token_payload


async def get_current_user_ws(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
) -> TokenData:
    """
    WebSocket-версия: токен из query-параметра.
    Для браузера: new WebSocket("ws://.../chat/...?token=eyJ...")
    """
    # Пробуем получить токен из query-параметра
    if token is None:
        token = websocket.query_params.get("token")

    if not token:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Missing authentication token. Use ?token=...",
        )

    try:
        return _validate_token_payload(token)
    except ValueError:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Invalid or expired token"
        )
