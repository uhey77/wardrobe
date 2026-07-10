import importlib

from backend.app.application.clothing_items import ItemVectorRepository, VectorSyncError
from backend.app.domain.item import ClothingItem


class ChromaItemVectorRepository(ItemVectorRepository):
    def __init__(self, host: str, port: int, collection_name: str) -> None:
        self._host = host
        self._port = port
        self._collection_name = collection_name

    def upsert(self, item: ClothingItem, embedding: list[float]) -> None:
        try:
            chromadb = importlib.import_module("chromadb")
            client_factory = chromadb.__dict__["HttpClient"]
            client = client_factory(host=self._host, port=self._port)
            collection = client.get_or_create_collection(name=self._collection_name)
            collection.upsert(
                ids=[item.id],
                embeddings=[embedding],
                metadatas=[_metadata_from_item(item)],
                documents=[item.attributes.description],
            )
        except Exception as exc:
            raise VectorSyncError(f"Chroma is unavailable: {exc}") from exc


def _metadata_from_item(item: ClothingItem) -> dict[str, str]:
    return {
        "category": item.attributes.category.value,
        "colors": ",".join(item.attributes.colors),
        "seasons": ",".join(season.value for season in item.attributes.seasons),
        "style_tags": ",".join(item.attributes.style_tags),
        "original_filename": item.original_filename,
        "image_path": item.image_path,
        "image_content_type": item.image_content_type,
        "created_at": item.created_at.isoformat(),
    }
