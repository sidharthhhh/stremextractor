import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables (or a backend/.env file).
    Every value has a sensible local-dev default so the app runs out of the box,
    while production deployments override them via real environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Server ---
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False          # enable auto-reload only in local dev
    debug: bool = False           # gates the /api/debug/* endpoints

    # --- CORS (comma-separated list of allowed origins) ---
    # e.g. "https://app.example.com,https://www.example.com"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Storage ---
    temp_dir: str = os.path.join(os.path.dirname(__file__), "temp")

    # --- Cleanup: seconds to keep a finished file before deleting it ---
    file_cleanup_delay: int = 5

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse the comma-separated CORS origins string into a clean list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Single shared settings instance imported across the backend.
settings = Settings()
