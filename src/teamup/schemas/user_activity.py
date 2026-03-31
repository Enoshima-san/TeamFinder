from base64 import b64encode
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from teamup.domain import Game


class ResponseOut(BaseModel):
    user_id: UUID
    announcement_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime = datetime.now()


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
