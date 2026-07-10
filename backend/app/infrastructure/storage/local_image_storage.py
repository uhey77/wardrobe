from pathlib import Path

from backend.app.application.clothing_items import ImageStorage
from backend.app.application.clothing_items.dtos import (
    StoredImageLocation,
    StoredImageMeta,
)

_CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class LocalImageStorage(ImageStorage):
    def __init__(self, storage_dir: Path) -> None:
        self._storage_dir = storage_dir

    def save(
        self,
        item_id: str,
        image_content: bytes,
        original_filename: str,
        content_type: str,
    ) -> StoredImageMeta:
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        storage_key = f"{item_id}{_CONTENT_TYPE_EXTENSIONS[content_type]}"
        destination = self._storage_dir / storage_key
        destination.write_bytes(image_content)
        return StoredImageMeta(
            storage_key=storage_key,
            content_type=content_type,
            size_bytes=len(image_content),
        )

    def get(self, storage_key: str, content_type: str) -> StoredImageLocation:
        root = self._storage_dir.resolve()
        path = (self._storage_dir / storage_key).resolve()
        if root != path.parent:
            raise FileNotFoundError(storage_key)
        if not path.is_file():
            raise FileNotFoundError(storage_key)
        return StoredImageLocation(path=path, content_type=content_type)
