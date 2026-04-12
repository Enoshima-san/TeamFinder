import pytest

from teamup.infra.external import ExternalApiHandler


@pytest.mark.asyncio
async def test_api():
    handler = ExternalApiHandler()
    res = await handler.get("https://www.cybersport.ru/players/cs2")

    assert res is not None, "Не удалось получить страницу"
