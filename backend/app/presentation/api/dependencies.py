from backend.app.application.phase0 import Phase0ServiceConfig, Phase0UseCase
from backend.app.core.config import get_settings


def get_phase0_use_case() -> Phase0UseCase:
    settings = get_settings()
    return Phase0UseCase(
        Phase0ServiceConfig(
            app_name=settings.app_name,
            environment=settings.environment,
            chroma_url=settings.chroma_url,
        )
    )
