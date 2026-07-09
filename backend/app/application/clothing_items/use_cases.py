from datetime import UTC, datetime
from uuid import uuid4

from backend.app.application.clothing_items.errors import (
    ClothingItemNotFoundError,
    InvalidImageError,
    StoredImageNotFoundError,
    VectorSyncError,
)
from backend.app.application.clothing_items.inputs import RegisterClothingItemInput
from backend.app.application.clothing_items.ports import (
    ClothingAttributeExtractor,
    ClothingItemRepository,
    ImageEmbeddingProvider,
    ImageStorage,
    ItemVectorRepository,
)
from backend.app.application.clothing_items.dtos import StoredImageLocation
from backend.app.application.clothing_items.results import RegistrationResult
from backend.app.domain.item import ClothingItem

ALLOWED_IMAGE_CONTENT_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})
DEFAULT_MAX_IMAGE_BYTES = 10 * 1024 * 1024


class RegisterClothingItemUseCase:
    def __init__(
        self,
        image_storage: ImageStorage,
        attribute_extractor: ClothingAttributeExtractor,
        embedding_provider: ImageEmbeddingProvider,
        item_repository: ClothingItemRepository,
        vector_repository: ItemVectorRepository,
        max_image_bytes: int = DEFAULT_MAX_IMAGE_BYTES,
    ) -> None:
        self._image_storage = image_storage
        self._attribute_extractor = attribute_extractor
        self._embedding_provider = embedding_provider
        self._item_repository = item_repository
        self._vector_repository = vector_repository
        self._max_image_bytes = max_image_bytes

    def register(self, input_data: RegisterClothingItemInput) -> RegistrationResult:
        content_type = input_data.content_type.split(";", maxsplit=1)[0].strip().lower()
        self._validate_image(input_data.image_content, content_type)

        item_id = str(uuid4())
        attributes = self._attribute_extractor.extract(
            image_content=input_data.image_content,
            original_filename=input_data.original_filename,
            content_type=content_type,
        )
        embedding = self._embedding_provider.embed(input_data.image_content, attributes)
        stored_image = self._image_storage.save(
            item_id=item_id,
            image_content=input_data.image_content,
            original_filename=input_data.original_filename,
            content_type=content_type,
        )
        item = ClothingItem(
            item_id=item_id,
            original_filename=input_data.original_filename,
            image_path=stored_image.storage_key,
            image_content_type=stored_image.content_type,
            attributes=attributes,
            created_at=datetime.now(UTC),
        )
        self._item_repository.save(item)

        vector_status = "synced"
        try:
            self._vector_repository.upsert(item, embedding)
        except VectorSyncError as exc:
            vector_status = f"skipped: {exc}"

        return RegistrationResult(item=item, vector_status=vector_status)

    def _validate_image(self, image_content: bytes, content_type: str) -> None:
        if not image_content:
            raise InvalidImageError("Image content must not be empty.")
        if len(image_content) > self._max_image_bytes:
            raise InvalidImageError("Image content is too large.")
        if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise InvalidImageError("Unsupported image content type.")


class ListClothingItemsUseCase:
    def __init__(self, item_repository: ClothingItemRepository) -> None:
        self._item_repository = item_repository

    def list_items(self) -> list[ClothingItem]:
        return self._item_repository.list_items()


class GetClothingItemImageUseCase:
    def __init__(
        self,
        image_storage: ImageStorage,
        item_repository: ClothingItemRepository,
    ) -> None:
        self._image_storage = image_storage
        self._item_repository = item_repository

    def get_image(self, item_id: str) -> StoredImageLocation:
        item = self._item_repository.get_by_id(item_id)
        if item is None:
            raise ClothingItemNotFoundError("Clothing item was not found.")

        try:
            return self._image_storage.get(item.image_path, item.image_content_type)
        except FileNotFoundError as exc:
            raise StoredImageNotFoundError("Stored image was not found.") from exc
