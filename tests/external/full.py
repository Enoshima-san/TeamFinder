import pytest

from teamup.infra.external import (
    CybersportRuScraper,
    ExternalApiHandler,
)

BASE_URL = "https://www.cybersport.ru/players/cs-go"


@pytest.mark.asyncio
async def test_full():
    handler = ExternalApiHandler()
    res = await handler.get(BASE_URL)
    assert res is not None
    scraper = CybersportRuScraper(res.text)
    results = scraper.parse_for_count(5)
    assert results
    print([el.model_dump() for el in results])
    print(len(results))
