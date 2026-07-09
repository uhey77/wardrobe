from abc import ABC, abstractmethod

from backend.app.domain.item import ClothingAttributes, ClothingItem

from backend.app.application.clothing_items.dtos import (
    StoredImageLocation,
    StoredImageMeta,
)


class ImageStorage(ABC):
    @abstractmethod
    def save(
        self,
        item_id: str,
        image_content: bytes,
        original_filename: str,
        content_type: str,
    ) -> StoredImageMeta:
        raise NotImplementedError

    @abstractmethod
    def get(self, storage_key: str, content_type: str) -> StoredImageLocation:
        raise NotImplementedError


class ClothingAttributeExtractor(ABC):
    @abstractmethod
    def extract(
        self,
        image_content: bytes,
        original_filename: str,
        content_type: str,
    ) -> ClothingAttributes:
        raise NotImplementedError


class ImageEmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, image_content: bytes, attributes: ClothingAttributes) -> list[float]:
        raise NotImplementedError


class ClothingItemRepository(ABC):
    @abstractmethod
    def save(self, item: ClothingItem) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_items(self) -> list[ClothingItem]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: str) -> ClothingItem | None:
        raise NotImplementedError


class ItemVectorRepository(ABC):
    @abstractmethod
    def upsert(self, item: ClothingItem, embedding: list[float]) -> None:
        raise NotImplementedError
