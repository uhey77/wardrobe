from backend.app.domain.item import ClothingItem


class RegistrationResult:
    def __init__(self, item: ClothingItem, vector_status: str) -> None:
        self._item = item
        self._vector_status = vector_status

    @property
    def item(self) -> ClothingItem:
        return self._item

    @property
    def vector_status(self) -> str:
        return self._vector_status
