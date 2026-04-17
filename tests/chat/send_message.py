from uuid import UUID

import pytest

from teamup.application.di import get_send_message_use_case
from teamup.domain import Message
from teamup.infra.database import get_db_session

xxx = UUID("00e12fc2-3cff-4e30-8a24-a658f030ab4e")
_xx = UUID("fd36f10c-6bb4-45ca-a9ca-2dbdabcd3dae")
conv_id = UUID("e373d928-e3e7-4ffd-ac6b-4e5c2a12bef4")


@pytest.mark.asyncio
async def test_send_message():
    message = Message.create(xxx, _xx, conv_id, "sex?")
    async with get_db_session() as db:
        sm_us = await get_send_message_use_case(db)
        res = await sm_us(message)
        print(res.content)
