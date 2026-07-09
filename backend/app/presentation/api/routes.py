from typing import Annotated
from urllib.parse import unquote

from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi.responses import FileResponse

from backend.app.application.clothing_items import (
    ClothingItemNotFoundError,
    GetClothingItemImageUseCase,
    InvalidImageError,
    ListClothingItemsUseCase,
    RegisterClothingItemInput,
    RegisterClothingItemUseCase,
    StoredImageNotFoundError,
)
from backend.app.application.service_status import ServiceStatusUseCase
from backend.app.presentation.api.dependencies import (
    get_clothing_item_image_use_case,
    get_list_clothing_items_use_case,
    get_register_clothing_item_use_case,
    get_service_status_use_case,
)
from backend.app.presentation.api.schemas import (
    ClothingItemResponse,
    ConnectivityResponse,
    HealthResponse,
    RegisterClothingItemResponse,
)

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health(
    use_case: Annotated[ServiceStatusUseCase, Depends(get_service_status_use_case)],
) -> HealthResponse:
    return HealthResponse.from_domain(use_case.get_health_status())


@router.get("/connectivity", response_model=ConnectivityResponse)
async def connectivity(
    use_case: Annotated[ServiceStatusUseCase, Depends(get_service_status_use_case)],
) -> ConnectivityResponse:
    return ConnectivityResponse.from_domain(use_case.get_connectivity_status())


@router.post("/items", response_model=RegisterClothingItemResponse, status_code=201)
async def register_item(
    image_content: Annotated[bytes, Body(media_type="application/octet-stream")],
    use_case: Annotated[
        RegisterClothingItemUseCase,
        Depends(get_register_clothing_item_use_case),
    ],
    content_type: Annotated[str | None, Header(alias="Content-Type")] = None,
    original_filename: Annotated[str | None, Header(alias="X-Wardrobe-Filename")] = None,
) -> RegisterClothingItemResponse:
    try:
        result = use_case.register(
            RegisterClothingItemInput(
                image_content=image_content,
                original_filename=_decode_filename(original_filename),
                content_type=content_type or "application/octet-stream",
            )
        )
    except InvalidImageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RegisterClothingItemResponse.from_result(result)


@router.get("/items", response_model=list[ClothingItemResponse])
async def list_items(
    use_case: Annotated[
        ListClothingItemsUseCase,
        Depends(get_list_clothing_items_use_case),
    ],
) -> list[ClothingItemResponse]:
    return [ClothingItemResponse.from_domain(item) for item in use_case.list_items()]


@router.get("/items/{item_id}/image", response_class=FileResponse)
async def get_item_image(
    item_id: str,
    use_case: Annotated[
        GetClothingItemImageUseCase,
        Depends(get_clothing_item_image_use_case),
    ],
) -> FileResponse:
    try:
        image = use_case.get_image(item_id)
    except (ClothingItemNotFoundError, StoredImageNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return FileResponse(path=image.path, media_type=image.content_type)


def _decode_filename(filename: str | None) -> str:
    if filename is None:
        return "upload"
    return unquote(filename).strip() or "upload"
