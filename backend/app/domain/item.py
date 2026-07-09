from datetime import UTC, datetime
from enum import StrEnum


class ClothingCategory(StrEnum):
    TOPS = "tops"
    BOTTOMS = "bottoms"
    OUTERWEAR = "outerwear"
    SHOES = "shoes"
    ACCESSORIES = "accessories"
    ONE_PIECE = "one_piece"
    UNKNOWN = "unknown"


class Season(StrEnum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class ClothingAttributes:
    def __init__(
        self,
        category: ClothingCategory,
        colors: list[str],
        seasons: list[Season],
        style_tags: list[str],
        description: str,
    ) -> None:
        self._category = category
        self._colors = _normalize_tokens(colors, "colors")
        self._seasons = seasons
        self._style_tags = _normalize_tokens(style_tags, "style_tags")
        self._description = description.strip()

        if not self._seasons:
            raise ValueError("seasons must not be empty")
        if not self._description:
            raise ValueError("description must not be empty")

    @classmethod
    def from_values(
        cls,
        category: str,
        colors: list[str],
        seasons: list[str],
        style_tags: list[str],
        description: str,
    ) -> "ClothingAttributes":
        return cls(
            category=ClothingCategory(category),
            colors=colors,
            seasons=[Season(season) for season in seasons],
            style_tags=style_tags,
            description=description,
        )

    @property
    def category(self) -> ClothingCategory:
        return self._category

    @property
    def colors(self) -> list[str]:
        return list(self._colors)

    @property
    def seasons(self) -> list[Season]:
        return list(self._seasons)

    @property
    def style_tags(self) -> list[str]:
        return list(self._style_tags)

    @property
    def description(self) -> str:
        return self._description


class ClothingItem:
    def __init__(
        self,
        item_id: str,
        original_filename: str,
        image_path: str,
        image_content_type: str,
        attributes: ClothingAttributes,
        created_at: datetime,
    ) -> None:
        self._id = _require_text(item_id, "item_id")
        self._original_filename = _require_text(original_filename, "original_filename")
        self._image_path = _require_text(image_path, "image_path")
        self._image_content_type = _require_text(image_content_type, "image_content_type")
        self._attributes = attributes
        self._created_at = _normalize_datetime(created_at)

    @property
    def id(self) -> str:
        return self._id

    @property
    def original_filename(self) -> str:
        return self._original_filename

    @property
    def image_path(self) -> str:
        return self._image_path

    @property
    def image_content_type(self) -> str:
        return self._image_content_type

    @property
    def attributes(self) -> ClothingAttributes:
        return self._attributes

    @property
    def created_at(self) -> datetime:
        return self._created_at


def _normalize_tokens(values: list[str], field_name: str) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for value in values:
        token = value.strip().lower()
        if not token or token in seen:
            continue
        normalized.append(token)
        seen.add(token)

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


def _require_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
