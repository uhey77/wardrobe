from backend.app.domain.status import ConnectivityStatus, HealthStatus


class ServiceStatusConfig:
    def __init__(self, app_name: str, environment: str, chroma_url: str) -> None:
        self._app_name = app_name
        self._environment = environment
        self._chroma_url = chroma_url

    @property
    def app_name(self) -> str:
        return self._app_name

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def chroma_url(self) -> str:
        return self._chroma_url


class ServiceStatusUseCase:
    def __init__(self, config: ServiceStatusConfig) -> None:
        self._config = config

    def get_health_status(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            service=self._config.app_name,
            environment=self._config.environment,
            chroma_url=self._config.chroma_url,
        )

    def get_connectivity_status(self) -> ConnectivityStatus:
        return ConnectivityStatus(
            message="Wardrobe backend is reachable.",
            item_registration_endpoint="/api/items",
        )
