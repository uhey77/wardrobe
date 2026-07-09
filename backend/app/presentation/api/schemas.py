from datetime import datetime

from pydantic import BaseModel

from backend.app.application.clothing_items import RegistrationResult
from backend.app.domain.item import ClothingAttributes, ClothingItem
from backend.app.domain.status import ConnectivityStatus, HealthStatus


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


class ConnectivityResponse(BaseModel):
    message: str
    item_registration_endpoint: str

    @classmethod
    def from_domain(cls, status: ConnectivityStatus) -> "ConnectivityResponse":
        return cls(
            message=status.message,
            item_registration_endpoint=status.item_registration_endpoint,
        )


class ClothingAttributesResponse(BaseModel):
    category: str
    colors: list[str]
    seasons: list[str]
    style_tags: list[str]
    description: str

    @classmethod
    def from_domain(cls, attributes: ClothingAttributes) -> "ClothingAttributesResponse":
        return cls(
            category=attributes.category.value,
            colors=attributes.colors,
            seasons=[season.value for season in attributes.seasons],
            style_tags=attributes.style_tags,
            description=attributes.description,
        )


class ClothingItemResponse(BaseModel):
    id: str
    original_filename: str
    image_url: str
    attributes: ClothingAttributesResponse
    created_at: datetime

    @classmethod
    def from_domain(cls, item: ClothingItem) -> "ClothingItemResponse":
        return cls(
            id=item.id,
            original_filename=item.original_filename,
            image_url=f"/api/items/{item.id}/image",
            attributes=ClothingAttributesResponse.from_domain(item.attributes),
            created_at=item.created_at,
        )


class RegisterClothingItemResponse(BaseModel):
    item: ClothingItemResponse
    vector_status: str

    @classmethod
    def from_result(cls, result: RegistrationResult) -> "RegisterClothingItemResponse":
        return cls(
            item=ClothingItemResponse.from_domain(result.item),
            vector_status=result.vector_status,
        )
