from pathlib import Path


class StoredImageMeta:
    def __init__(self, storage_key: str, content_type: str, size_bytes: int) -> None:
        self._storage_key = storage_key
        self._content_type = content_type
        self._size_bytes = size_bytes

    @property
    def storage_key(self) -> str:
        return self._storage_key

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def size_bytes(self) -> int:
        return self._size_bytes


class StoredImageLocation:
    def __init__(self, path: Path, content_type: str) -> None:
        self._path = path
        self._content_type = content_type

    @property
    def path(self) -> Path:
        return self._path

    @property
    def content_type(self) -> str:
        return self._content_type
