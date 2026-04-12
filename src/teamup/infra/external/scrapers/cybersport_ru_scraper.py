import re
from typing import Optional

from bs4 import BeautifulSoup

from teamup.core import get_logger
from teamup.schemas import Player

logger = get_logger()


class CybersportRuScraper:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "lxml")
        self.soup_cards = [
            BeautifulSoup(str(i), "lxml") for i in self.soup.find_all("tr")
        ]
        self.soup_cards.pop(0)

    def parse(self) -> Player:
        """Возвращает только строки <tr>, которые содержат данные игрока"""
        soup_card = self.soup_cards.pop(0)
        return Player(
            nickname=self._get_player_nickname(soup_card),
            disclipline=self._get_disciplines_titles(self._get_disciplines(soup_card)),
            team=self._get_team(soup_card),
            stats=self._get_stats(soup_card),
            total_money=self._get_total_prize_money(soup_card),
        )

    def parse_for_count(self, top_cnt: int = 5) -> list[Player]:
        return [self.parse() for _ in range(top_cnt)]

    def _get_safe_text(self, elem) -> Optional[str]:
        """Безопасное получение текста без пробелов и переносов"""
        return elem.get_text(strip=True) if elem else None

    def _get_player_nickname(self, soup: BeautifulSoup) -> Optional[str]:
        nickname_el = soup.find("div", class_=re.compile(r"^nickname_"))
        return self._get_safe_text(nickname_el)

    def _get_player_name(self, soup: BeautifulSoup) -> Optional[str]:
        name_el = soup.find("div", class_=re.compile(r"^name_"))
        return self._get_safe_text(name_el)

    def _get_disciplines(self, soup: BeautifulSoup) -> list:
        return soup.find_all("a", class_=re.compile(r"^discipline_"))

    def _get_disciplines_titles(self, disciplines: list) -> list:
        return [d.get("title") for d in disciplines if d.get("title") is not None]

    def _get_team(self, soup: BeautifulSoup) -> Optional[str]:
        team_el = soup.find("div", class_=re.compile(r"^team_"))
        return self._get_safe_text(team_el)

    def _get_total_prize_money(self, soup: BeautifulSoup) -> Optional[str]:
        money = soup.find("td", class_=re.compile(r"^cellTotal"))
        return self._get_safe_text(money)

    def _get_stats(self, soup: BeautifulSoup) -> dict[str, Optional[int]]:
        green_s = soup.find("div", class_=re.compile(r"^percentItem_\S+\s+green_"))
        gray_s = soup.find("div", class_=re.compile(r"^percentItem_\S+\s+gray_"))
        red_s = soup.find("div", class_=re.compile(r"^percentItem_\S+\s+red_"))

        return {
            "wins": int(self._get_safe_text(green_s).split(" ")[0])
            if green_s
            else None,
            "losses": int(self._get_safe_text(red_s).split(" ")[0]) if red_s else None,
            "draws": int(self._get_safe_text(gray_s).split(" ")[1]) if gray_s else None,
        }
