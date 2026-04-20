from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from teamup.domain import WebSocketErrorType


class WebSocketMessageIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

    model_config = ConfigDict(extra="forbid")


class WebSocketErrorOut(BaseModel):
    type: WebSocketErrorType
    message: str
    field: Optional[str] = None
    code: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
