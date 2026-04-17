from uuid import UUID

import pytest

from teamup.core.di import get_message_repository
from teamup.infra.database import get_db_session


@pytest.mark.asyncio
async def test_get_conversation():
    async with get_db_session() as db:
        mess_r = await get_message_repository(db)
        res = await mess_r.get_by_conversation_id(
            UUID("e373d928-e3e7-4ffd-ac6b-4e5c2a12bef4")
        )
        assert res
        s = [({r.content}, {r.sender_id}, {r.recipient_id}) for r in res]
        s.reverse()
        for i in s:
            print(i)
