from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Wardrobe API"
    environment: str = "local"
    frontend_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_collection_name: str = "wardrobe_items"
    data_dir: Path = Path(".data")
    upload_dir_name: str = "uploads"
    items_store_filename: str = "items.json"
    max_image_bytes: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="WARDROBE_",
        extra="ignore",
    )

    @property
    def chroma_url(self) -> str:
        return f"http://{self.chroma_host}:{self.chroma_port}"

    @property
    def upload_dir(self) -> Path:
        return self.data_dir / self.upload_dir_name

    @property
    def items_store_path(self) -> Path:
        return self.data_dir / self.items_store_filename


@lru_cache
def get_settings() -> Settings:
    return Settings()
