from teamup.core import get_settings
from teamup.infra.external import CybersportRuScraper, ExternalApiHandler
from teamup.schemas import Player

from ...exceptions import ExternalApiError


class GetTopPlayersUseCase:
    def __init__(self, game_name: str):
        settings = get_settings()
        url = settings.external_api.get_cyber_sport_ru()
        self._url = f"{url}/{game_name}"

    async def __call__(self, players_cnt: int = 5) -> list[Player]:
        try:
            handler = ExternalApiHandler()
            res = await handler.get(self._url)
            if res is None:
                raise ExternalApiError("Сторонний сервис не отвечает")
            scraper = CybersportRuScraper(res.text)
            players = scraper.parse_for_count(players_cnt)
            return players
        except ExternalApiError:
            raise ExternalApiError("Сторонний сервис не отвечает")
        except Exception:
            raise Exception("Внутренняя ошибка сервера")
