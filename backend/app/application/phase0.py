from dataclasses import dataclass

from backend.app.domain.status import HealthStatus, Phase0Status


@dataclass(frozen=True)
class Phase0ServiceConfig:
    app_name: str
    environment: str
    chroma_url: str


class Phase0UseCase:
    def __init__(self, config: Phase0ServiceConfig) -> None:
        self._config = config

    def get_health_status(self) -> HealthStatus:
        return HealthStatus(
            status="ok",
            service=self._config.app_name,
            environment=self._config.environment,
            chroma_url=self._config.chroma_url,
        )

    def get_connectivity_status(self) -> Phase0Status:
        return Phase0Status(
            message="Wardrobe backend is reachable.",
            next_phase="Phase 1: item upload pipeline",
        )
