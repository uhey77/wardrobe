from pydantic import BaseModel

from backend.app.domain.status import HealthStatus, Phase0Status


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    chroma_url: str

    @classmethod
    def from_domain(cls, status: HealthStatus) -> "HealthResponse":
        return cls(
            status=status.status,
            service=status.service,
            environment=status.environment,
            chroma_url=status.chroma_url,
        )


class Phase0Response(BaseModel):
    message: str
    next_phase: str

    @classmethod
    def from_domain(cls, status: Phase0Status) -> "Phase0Response":
        return cls(message=status.message, next_phase=status.next_phase)
