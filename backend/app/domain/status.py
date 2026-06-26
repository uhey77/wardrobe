from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatus:
    status: str
    service: str
    environment: str
    chroma_url: str


@dataclass(frozen=True)
class Phase0Status:
    message: str
    next_phase: str
