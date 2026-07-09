from backend.app.application.clothing_items import (
    GetClothingItemImageUseCase,
    ListClothingItemsUseCase,
    RegisterClothingItemUseCase,
)
from backend.app.application.service_status import ServiceStatusConfig, ServiceStatusUseCase
from backend.app.core.config import get_settings
from backend.app.infrastructure.embedding.deterministic_image_embedding_provider import (
    DeterministicImageEmbeddingProvider,
)
from backend.app.infrastructure.storage.json_clothing_item_repository import (
    JsonClothingItemRepository,
)
from backend.app.infrastructure.storage.local_image_storage import LocalImageStorage
from backend.app.infrastructure.vector.chroma_item_vector_repository import (
    ChromaItemVectorRepository,
)
from backend.app.infrastructure.vision.rule_based_attribute_extractor import (
    RuleBasedClothingAttributeExtractor,
)


def get_service_status_use_case() -> ServiceStatusUseCase:
    settings = get_settings()
    return ServiceStatusUseCase(
        ServiceStatusConfig(
            app_name=settings.app_name,
            environment=settings.environment,
            chroma_url=settings.chroma_url,
        )
    )


def get_register_clothing_item_use_case() -> RegisterClothingItemUseCase:
    settings = get_settings()
    return RegisterClothingItemUseCase(
        image_storage=LocalImageStorage(settings.upload_dir),
        attribute_extractor=RuleBasedClothingAttributeExtractor(),
        embedding_provider=DeterministicImageEmbeddingProvider(),
        item_repository=JsonClothingItemRepository(settings.items_store_path),
        vector_repository=ChromaItemVectorRepository(
            host=settings.chroma_host,
            port=settings.chroma_port,
            collection_name=settings.chroma_collection_name,
        ),
        max_image_bytes=settings.max_image_bytes,
    )


def get_list_clothing_items_use_case() -> ListClothingItemsUseCase:
    settings = get_settings()
    return ListClothingItemsUseCase(
        item_repository=JsonClothingItemRepository(settings.items_store_path),
    )


def get_clothing_item_image_use_case() -> GetClothingItemImageUseCase:
    settings = get_settings()
    return GetClothingItemImageUseCase(
        image_storage=LocalImageStorage(settings.upload_dir),
        item_repository=JsonClothingItemRepository(settings.items_store_path),
    )
