from typing import Optional

from pydantic import BaseModel


class Player(BaseModel):
    nickname: Optional[str]
    disclipline: list[str]
    team: Optional[str]
    stats: dict
    total_money: Optional[str]
