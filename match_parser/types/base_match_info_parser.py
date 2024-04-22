from abc import ABC, abstractmethod

from .match import Match


class BaseMatchInfoParser(ABC):
    """
    Базовый класс. Парсинг информации о матче
    """

    @abstractmethod
    def parse(self, base_url: str, match: Match) -> tuple[str, str]:
        pass
