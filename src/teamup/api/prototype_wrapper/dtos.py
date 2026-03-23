from uuid import UUID

from pydantic import BaseModel


class ResponseCreateIn(BaseModel):
    announcement_id: UUID
