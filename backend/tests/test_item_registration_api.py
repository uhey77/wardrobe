from collections.abc import Iterator
from pathlib import Path

import pytest
from backend.app.application.clothing_items import (
    GetClothingItemImageUseCase,
    ImageEmbeddingProvider,
    ItemVectorRepository,
    ListClothingItemsUseCase,
    RegisterClothingItemUseCase,
)
from backend.app.domain.item import ClothingItem
from backend.app.infrastructure.embedding.deterministic_image_embedding_provider import (
    DeterministicImageEmbeddingProvider,
)
from backend.app.infrastructure.storage.json_clothing_item_repository import (
    JsonClothingItemRepository,
)
from backend.app.infrastructure.storage.local_image_storage import LocalImageStorage
from backend.app.infrastructure.vision.rule_based_attribute_extractor import (
    RuleBasedClothingAttributeExtractor,
)
from backend.app.main import app
from backend.app.presentation.api.dependencies import (
    get_clothing_item_image_use_case,
    get_list_clothing_items_use_case,
    get_register_clothing_item_use_case,
)
from fastapi.testclient import TestClient

client = TestClient(app)
PNG_BYTES = b"\x89PNG\r\n\x1a\nwardrobe-test-image"


class NoopItemVectorRepository(ItemVectorRepository):
    def __init__(self) -> None:
        self.synced_item_ids: list[str] = []

    def upsert(self, item: ClothingItem, embedding: list[float]) -> None:
        self.synced_item_ids.append(item.id)


@pytest.fixture()
def item_registration_overrides(tmp_path: Path) -> Iterator[None]:
    storage = LocalImageStorage(tmp_path / "uploads")
    repository = JsonClothingItemRepository(tmp_path / "items.json")
    embedding_provider: ImageEmbeddingProvider = DeterministicImageEmbeddingProvider()
    vector_repository = NoopItemVectorRepository()

    def register_use_case() -> RegisterClothingItemUseCase:
        return RegisterClothingItemUseCase(
            image_storage=storage,
            attribute_extractor=RuleBasedClothingAttributeExtractor(),
            embedding_provider=embedding_provider,
            item_repository=repository,
            vector_repository=vector_repository,
        )

    def list_use_case() -> ListClothingItemsUseCase:
        return ListClothingItemsUseCase(item_repository=repository)

    def image_use_case() -> GetClothingItemImageUseCase:
        return GetClothingItemImageUseCase(image_storage=storage, item_repository=repository)

    app.dependency_overrides[get_register_clothing_item_use_case] = register_use_case
    app.dependency_overrides[get_list_clothing_items_use_case] = list_use_case
    app.dependency_overrides[get_clothing_item_image_use_case] = image_use_case

    yield

    app.dependency_overrides.clear()


def test_register_item_uploads_image_and_lists_auto_tagged_item(
    item_registration_overrides: None,
) -> None:
    response = client.post(
        "/api/items",
        content=PNG_BYTES,
        headers={
            "Content-Type": "image/png",
            "X-Wardrobe-Filename": "blue-shirt.png",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    item = payload["item"]

    assert payload["vector_status"] == "synced"
    assert item["original_filename"] == "blue-shirt.png"
    assert item["image_url"] == f"/api/items/{item['id']}/image"
    assert item["attributes"] == {
        "category": "tops",
        "colors": ["blue"],
        "seasons": ["spring", "autumn"],
        "style_tags": ["clean"],
        "description": "Auto-tagged blue tops item from blue-shirt.png.",
    }

    list_response = client.get("/api/items")

    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["id"] == item["id"]
    assert items[0]["attributes"]["colors"] == ["blue"]

    image_response = client.get(item["image_url"])

    assert image_response.status_code == 200
    assert image_response.content == PNG_BYTES
    assert image_response.headers["content-type"] == "image/png"


def test_register_item_rejects_unsupported_content_type(
    item_registration_overrides: None,
) -> None:
    response = client.post(
        "/api/items",
        content=b"not an image",
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported image content type."}
