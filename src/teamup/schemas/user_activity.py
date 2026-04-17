from base64 import b64encode
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Conversation, Game, Message, Response

from .brief_dto import ConversationBriefDto


class ResponseOut(BaseModel):
    user_id: UUID
    announcement_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime = datetime.now()


class ResponseCreationIn(BaseModel):
    message: str


class ResponseCreationOut(BaseModel):
    user_id: UUID
    announcement_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime = datetime.now()

    initial_conversation: ConversationBriefDto

    @staticmethod
    def create(
        response: Response,
        conversation: Conversation,
        message: Message,
    ) -> "ResponseCreationOut":
        return ResponseCreationOut(
            user_id=response.user_id,
            announcement_id=response.announcement_id,
            status=response.status,
            created_at=response.created_at,
            initial_conversation=ConversationBriefDto.from_conversation(
                conversation, message
            ),
        )


class GameResponse(BaseModel):
    game_id: UUID
    game_name: str
    game_icon: str

    @staticmethod
    def create(g: Game) -> "GameResponse":
        return GameResponse(
            game_id=g.game_id,
            game_name=g.game_name,
            game_icon=b64encode(g.game_icon).decode(),
        )
