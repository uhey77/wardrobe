import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict, cast

from backend.app.application.clothing_items import ClothingItemRepository
from backend.app.domain.item import ClothingAttributes, ClothingItem


class _AttributesRecord(TypedDict):
    category: str
    colors: list[str]
    seasons: list[str]
    style_tags: list[str]
    description: str


class _ItemRecord(TypedDict):
    id: str
    original_filename: str
    image_path: str
    image_content_type: str
    attributes: _AttributesRecord
    created_at: str


class _StoreRecord(TypedDict):
    items: list[_ItemRecord]


class JsonClothingItemRepository(ClothingItemRepository):
    def __init__(self, store_path: Path) -> None:
        self._store_path = store_path

    def save(self, item: ClothingItem) -> None:
        records = [record for record in self._load_records() if record.get("id") != item.id]
        records.append(_record_from_item(item))
        self._write_records(records)

    def list_items(self) -> list[ClothingItem]:
        items: list[ClothingItem] = []
        for record in self._load_records():
            try:
                items.append(_item_from_record(record))
            except (KeyError, TypeError, ValueError):
                continue
        return sorted(items, key=lambda item: item.created_at, reverse=True)

    def get_by_id(self, item_id: str) -> ClothingItem | None:
        return next((item for item in self.list_items() if item.id == item_id), None)

    def _load_records(self) -> list[_ItemRecord]:
        if not self._store_path.exists():
            return []

        data = json.loads(self._store_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return []

        raw_items = data.get("items", [])
        if not isinstance(raw_items, list):
            return []

        return [cast(_ItemRecord, item) for item in raw_items if isinstance(item, dict)]

    def _write_records(self, records: list[_ItemRecord]) -> None:
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        payload: _StoreRecord = {"items": records}
        temp_path = self._store_path.with_suffix(f"{self._store_path.suffix}.tmp")
        temp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(self._store_path)


def _record_from_item(item: ClothingItem) -> _ItemRecord:
    return {
        "id": item.id,
        "original_filename": item.original_filename,
        "image_path": item.image_path,
        "image_content_type": item.image_content_type,
        "attributes": {
            "category": item.attributes.category.value,
            "colors": item.attributes.colors,
            "seasons": [season.value for season in item.attributes.seasons],
            "style_tags": item.attributes.style_tags,
            "description": item.attributes.description,
        },
        "created_at": item.created_at.isoformat(),
    }


def _item_from_record(record: _ItemRecord) -> ClothingItem:
    attributes = record["attributes"]
    return ClothingItem(
        item_id=record["id"],
        original_filename=record["original_filename"],
        image_path=record["image_path"],
        image_content_type=record["image_content_type"],
        attributes=ClothingAttributes.from_values(
            category=attributes["category"],
            colors=attributes["colors"],
            seasons=attributes["seasons"],
            style_tags=attributes["style_tags"],
            description=attributes["description"],
        ),
        created_at=datetime.fromisoformat(record["created_at"]),
    )
