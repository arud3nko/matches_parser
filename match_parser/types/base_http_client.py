from abc import ABC, abstractmethod

from requests import Response


class BaseHTTPClient(ABC):
    """HTTP-клиент"""
    @abstractmethod
    def get(self, url: str, **kwargs) -> Response:
        pass

    @abstractmethod
    def post(self, url: str, **kwargs) -> Response:
        pass
