from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from teamup.core.di import get_message_repository


@pytest.mark.asyncio
async def test_get_conversation(db_session: AsyncSession):
    message_repo = await get_message_repository(db_session)

    conversation_id = UUID("e373d928-e3e7-4ffd-ac6b-4e5c2a12bef4")
    messages = await message_repo.get_by_conversation_id(conversation_id)

    assert messages is not None, "Сообщения не найдены"
    assert len(messages) > 0, "Конверсация пуста"

    formatted = [(msg.content, msg.sender_id, msg.recipient_id) for msg in messages]
    formatted.reverse()

    print(f"\n📨 Найдено сообщений: {len(formatted)}")
    for content, sender, recipient in formatted:
        print(f"   • {sender} → {recipient}: {content}")
