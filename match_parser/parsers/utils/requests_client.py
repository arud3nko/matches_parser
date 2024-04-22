import requests

from requests import Response

from ...types import BaseHTTPClient


class RequestsClient(BaseHTTPClient):
    """
    Request method.
    url – URL for the new Request object.
    **kwargs:
        params – (optional) Dictionary, list of tuples or bytes to send in the query string for the Request. # noqa
        json – (optional) A JSON serializable Python object to send in the body of the Request. # noqa
        headers – (optional) Dictionary of HTTP Headers to send with the Request.
    """

    def get(self, url: str, **kwargs) -> Response:
        return requests.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return requests.post(url, **kwargs)
