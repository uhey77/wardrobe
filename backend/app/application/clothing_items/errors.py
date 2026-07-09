class ItemRegistrationError(Exception):
    pass


class InvalidImageError(ItemRegistrationError):
    pass


class ClothingItemNotFoundError(ItemRegistrationError):
    pass


class StoredImageNotFoundError(ItemRegistrationError):
    pass


class VectorSyncError(ItemRegistrationError):
    pass
