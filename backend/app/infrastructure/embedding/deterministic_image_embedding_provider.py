import hashlib
import math

from backend.app.application.clothing_items import ImageEmbeddingProvider
from backend.app.domain.item import ClothingAttributes

_EMBEDDING_SIZE = 64


class DeterministicImageEmbeddingProvider(ImageEmbeddingProvider):
    def embed(self, image_content: bytes, attributes: ClothingAttributes) -> list[float]:
        attribute_text = "|".join(
            [
                attributes.category.value,
                ",".join(attributes.colors),
                ",".join(season.value for season in attributes.seasons),
                ",".join(attributes.style_tags),
                attributes.description,
            ]
        )
        seed = image_content + attribute_text.encode("utf-8")
        digest = hashlib.blake2b(seed, digest_size=_EMBEDDING_SIZE).digest()
        values = [(byte / 255.0) * 2.0 - 1.0 for byte in digest]
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return [round(value / norm, 6) for value in values]
