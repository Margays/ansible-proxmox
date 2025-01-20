from ..client import Client


class BaseHandler:
    def __init__(self, client: type[Client]) -> None:
        self._client_class = client
