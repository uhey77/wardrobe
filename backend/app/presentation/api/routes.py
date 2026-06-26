from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.application.phase0 import Phase0UseCase
from backend.app.presentation.api.dependencies import get_phase0_use_case
from backend.app.presentation.api.schemas import HealthResponse, Phase0Response

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health(
    use_case: Annotated[Phase0UseCase, Depends(get_phase0_use_case)],
) -> HealthResponse:
    return HealthResponse.from_domain(use_case.get_health_status())


@router.get("/phase0", response_model=Phase0Response)
async def phase0(
    use_case: Annotated[Phase0UseCase, Depends(get_phase0_use_case)],
) -> Phase0Response:
    return Phase0Response.from_domain(use_case.get_connectivity_status())
