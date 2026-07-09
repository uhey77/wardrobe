class RegisterClothingItemInput:
    def __init__(self, image_content: bytes, original_filename: str, content_type: str) -> None:
        self._image_content = image_content
        self._original_filename = original_filename.strip() or "upload"
        self._content_type = content_type.strip().lower()

    @property
    def image_content(self) -> bytes:
        return self._image_content

    @property
    def original_filename(self) -> str:
        return self._original_filename

    @property
    def content_type(self) -> str:
        return self._content_type
