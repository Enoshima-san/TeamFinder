from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.application.di import get_send_message_use_case
from teamup.core.di import get_message_repository
from teamup.domain import Message

SENDER_ID = UUID("00e12fc2-3cff-4e30-8a24-a658f030ab4e")
RECIPIENT_ID = UUID("fd36f10c-6bb4-45ca-a9ca-2dbdabcd3dae")
CONV_ID = UUID("e373d928-e3e7-4ffd-ac6b-4e5c2a12bef4")


@pytest.mark.asyncio
async def test_send_message(db_session: AsyncSession):
    message = Message.create(SENDER_ID, RECIPIENT_ID, CONV_ID, "kak dela?")

    message_repo = await get_message_repository(db_session)
    send_message_uc = await get_send_message_use_case(message_repo)

    result = await send_message_uc(message)

    assert result is not None
    assert result.content == "kak dela?"
    assert result.sender_id == SENDER_ID
