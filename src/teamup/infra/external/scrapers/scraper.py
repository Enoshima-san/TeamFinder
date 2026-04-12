from abc import ABC, abstractmethod
from typing import Optional


class Scraper(ABC):
    @abstractmethod
    def parse(self, html: Optional[str] = None) -> list:
        """
        Парсит весь html и возвращает список всех совпадений
        """
        ...

    @abstractmethod
    def parse_target(self, it) -> dict:
        """
        Парсит одно итерируемое совпадение, которое обнаружил `parse()`
        """
        ...
