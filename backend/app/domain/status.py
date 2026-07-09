class HealthStatus:
    def __init__(self, status: str, service: str, environment: str, chroma_url: str) -> None:
        self._status = status
        self._service = service
        self._environment = environment
        self._chroma_url = chroma_url

    @property
    def status(self) -> str:
        return self._status

    @property
    def service(self) -> str:
        return self._service

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def chroma_url(self) -> str:
        return self._chroma_url


class ConnectivityStatus:
    def __init__(self, message: str, item_registration_endpoint: str) -> None:
        self._message = message
        self._item_registration_endpoint = item_registration_endpoint

    @property
    def message(self) -> str:
        return self._message

    @property
    def item_registration_endpoint(self) -> str:
        return self._item_registration_endpoint
