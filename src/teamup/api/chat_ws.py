from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from pydantic import ValidationError

from teamup.application.di import (
    get_check_conversation_access_use_case,
    get_send_message_use_case,
)
from teamup.application.exceptions import ForbiddenError
from teamup.application.use_cases import (
    CheckConversationAccessUseCase,
    SendMessageUseCase,
)
from teamup.core import get_logger
from teamup.core.di import get_current_user_ws
from teamup.domain import Message, WebSocketErrorType
from teamup.infra.websocket import manager
from teamup.schemas import (
    TokenData,
    WebSocketErrorOut,
    WebSocketMessageIn,
)

chat_ws_router = APIRouter(prefix="/ws", tags=["chat"])

logger = get_logger()


@chat_ws_router.websocket("/chat/{announcement_id}/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: UUID,
    announcement_id: UUID,
    ca_uc: CheckConversationAccessUseCase = Depends(
        get_check_conversation_access_use_case
    ),
    sm_uc: SendMessageUseCase = Depends(get_send_message_use_case),
    token_data: TokenData = Depends(get_current_user_ws),
):
    await websocket.accept()
    await manager.add_connection(websocket, conversation_id)

    conversation, announcement = await ca_uc(
        conversation_id=conversation_id,
        announcement_id=announcement_id,
        user_id=token_data.user_id,
    )

    try:
        while True:
            raw_data = await websocket.receive_json()

            try:
                validated = WebSocketMessageIn(**raw_data)
            except ValidationError as e:
                err = e.errors()[0]
                error_response = WebSocketErrorOut(
                    type=WebSocketErrorType.VALIDATION,
                    message=err["msg"],
                    field=".".join(map(str, err.get("loc", []))),
                )
                await websocket.send_json(error_response.model_dump())
                continue

            try:
                sender_id = token_data.user_id
                recipient_id = conversation.get_other_participant(sender_id)

                message = Message.create(
                    conversation_id=conversation_id,
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    content=validated.content,
                )
                saved_message = await sm_uc(message)
                payload = {
                    "type": "new_message",
                    "message_id": str(saved_message.message_id),
                    "conversation_id": str(saved_message.conversation_id),
                    "sender_id": str(saved_message.sender_id),
                    "content": saved_message.content,
                    "created_at": saved_message.created_at.isoformat(),
                }

                await manager.broadcast(conversation_id, payload)

            except ForbiddenError as e:
                logger.warning(f"Access denied during chat: {e}")
                await websocket.close(
                    code=status.WS_1008_POLICY_VIOLATION, reason=str(e)
                )
                return

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_json(
                    {
                        "type": "error",
                        "message": "Не удалось отправить сообщение. Попробуйте позже.",
                    }
                )

    except WebSocketDisconnect:
        manager.remove_connection(websocket, conversation_id)
        logger.info(f"Client disconnected from {conversation_id}")

    except Exception as e:
        logger.error(f"Fatal websocket error: {e}")
        manager.remove_connection(websocket, conversation_id)
