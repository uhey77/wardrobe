"""Application services for clothing item workflows."""

from backend.app.application.clothing_items.errors import (
    ClothingItemNotFoundError,
    InvalidImageError,
    ItemRegistrationError,
    StoredImageNotFoundError,
    VectorSyncError,
)
from backend.app.application.clothing_items.inputs import RegisterClothingItemInput
from backend.app.application.clothing_items.dtos import (
    StoredImageLocation,
    StoredImageMeta,
)
from backend.app.application.clothing_items.ports import (
    ClothingAttributeExtractor,
    ClothingItemRepository,
    ImageEmbeddingProvider,
    ImageStorage,
    ItemVectorRepository,
)
from backend.app.application.clothing_items.results import RegistrationResult
from backend.app.application.clothing_items.use_cases import (
    GetClothingItemImageUseCase,
    ListClothingItemsUseCase,
    RegisterClothingItemUseCase,
)

__all__ = [
    "ClothingAttributeExtractor",
    "ClothingItemNotFoundError",
    "ClothingItemRepository",
    "GetClothingItemImageUseCase",
    "ImageEmbeddingProvider",
    "ImageStorage",
    "InvalidImageError",
    "ItemRegistrationError",
    "ItemVectorRepository",
    "ListClothingItemsUseCase",
    "RegisterClothingItemInput",
    "RegisterClothingItemUseCase",
    "RegistrationResult",
    "StoredImageLocation",
    "StoredImageMeta",
    "StoredImageNotFoundError",
    "VectorSyncError",
]
