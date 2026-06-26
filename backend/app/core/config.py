from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Wardrobe API"
    environment: str = "local"
    frontend_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    chroma_host: str = "localhost"
    chroma_port: int = 8001

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="WARDROBE_",
        extra="ignore",
    )

    @property
    def chroma_url(self) -> str:
        return f"http://{self.chroma_host}:{self.chroma_port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
