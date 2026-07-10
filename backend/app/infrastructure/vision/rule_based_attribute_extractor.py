import hashlib

from backend.app.application.clothing_items import ClothingAttributeExtractor
from backend.app.domain.item import ClothingAttributes, ClothingCategory, Season

_CATEGORY_KEYWORDS: dict[ClothingCategory, set[str]] = {
    ClothingCategory.TOPS: {"shirt", "tee", "tshirt", "top", "blouse", "knit", "sweater"},
    ClothingCategory.BOTTOMS: {"pants", "jeans", "skirt", "shorts", "trouser"},
    ClothingCategory.OUTERWEAR: {"coat", "jacket", "outer", "blazer", "parka"},
    ClothingCategory.SHOES: {"shoe", "sneaker", "boot", "loafer", "sandal"},
    ClothingCategory.ACCESSORIES: {"bag", "belt", "hat", "cap", "scarf", "watch"},
    ClothingCategory.ONE_PIECE: {"dress", "onepiece", "one-piece"},
}

_COLOR_KEYWORDS = {
    "black": {"black", "bk"},
    "white": {"white", "ivory", "cream", "wt"},
    "gray": {"gray", "grey", "charcoal"},
    "navy": {"navy"},
    "blue": {"blue", "denim"},
    "green": {"green", "khaki", "olive"},
    "red": {"red", "wine", "burgundy"},
    "pink": {"pink"},
    "yellow": {"yellow", "mustard"},
    "brown": {"brown", "beige", "camel"},
}

_SEASON_KEYWORDS: dict[Season, set[str]] = {
    Season.SPRING: {"spring"},
    Season.SUMMER: {"summer"},
    Season.AUTUMN: {"autumn", "fall"},
    Season.WINTER: {"winter"},
}

_STYLE_KEYWORDS = {
    "casual": {"casual", "denim", "tee", "sneaker"},
    "clean": {"clean", "shirt", "blouse", "white"},
    "formal": {"formal", "suit", "blazer", "loafer"},
    "sporty": {"sport", "sneaker", "parka"},
    "minimal": {"plain", "minimal", "simple"},
}

_FALLBACK_COLORS = ["black", "white", "navy", "gray", "blue", "brown"]


class RuleBasedClothingAttributeExtractor(ClothingAttributeExtractor):
    def extract(
        self,
        image_content: bytes,
        original_filename: str,
        content_type: str,
    ) -> ClothingAttributes:
        filename = original_filename.lower()
        category = _detect_category(filename)
        colors = _detect_colors(filename, image_content)
        seasons = _detect_seasons(filename, category)
        style_tags = _detect_style_tags(filename)
        description = f"Auto-tagged {colors[0]} {category.value} item from {original_filename}."

        return ClothingAttributes(
            category=category,
            colors=colors,
            seasons=seasons,
            style_tags=style_tags,
            description=description,
        )


def _detect_category(filename: str) -> ClothingCategory:
    return next(
        (
            category
            for category, keywords in _CATEGORY_KEYWORDS.items()
            if any(keyword in filename for keyword in keywords)
        ),
        ClothingCategory.UNKNOWN,
    )


def _detect_colors(filename: str, image_content: bytes) -> list[str]:
    colors = [
        color
        for color, keywords in _COLOR_KEYWORDS.items()
        if any(keyword in filename for keyword in keywords)
    ]
    if colors:
        return colors

    digest = hashlib.blake2s(image_content, digest_size=1).digest()[0]
    return [_FALLBACK_COLORS[digest % len(_FALLBACK_COLORS)]]


def _detect_seasons(filename: str, category: ClothingCategory) -> list[Season]:
    seasons = [
        season
        for season, keywords in _SEASON_KEYWORDS.items()
        if any(keyword in filename for keyword in keywords)
    ]
    if seasons:
        return seasons

    if category in {ClothingCategory.OUTERWEAR}:
        return [Season.AUTUMN, Season.WINTER]
    if category in {ClothingCategory.SHOES, ClothingCategory.ACCESSORIES}:
        return [Season.SPRING, Season.SUMMER, Season.AUTUMN, Season.WINTER]
    return [Season.SPRING, Season.AUTUMN]


def _detect_style_tags(filename: str) -> list[str]:
    style_tags = [
        style_tag
        for style_tag, keywords in _STYLE_KEYWORDS.items()
        if any(keyword in filename for keyword in keywords)
    ]
    return style_tags or ["casual"]
