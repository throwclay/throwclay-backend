# apps/api/app/settings.py
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices, computed_field
from dotenv import load_dotenv, find_dotenv
import json
from typing import List

# Load nearest .env regardless of CWD
load_dotenv(find_dotenv(usecwd=True))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",          # ignore unknown keys in your .env
        case_sensitive=False,
    )

    # Core
    app_name: str = "ThrowClay API"
    version: str = "0.1.0"
    database_url: str  # DATABASE_URL

    # Optional extras we already have in .env
    supabase_url: str | None = None                 # SUPABASE_URL
    supabase_service_role_key: str | None = None    # SUPABASE_SERVICE_ROLE_KEY
    supabase_jwt_secret: str | None = None  # env: SUPABASE_JWT_SECRET

    # Read raw CORS env (string or list), then normalize
    cors_origins_raw: str | List[str] | None = Field(
        default=None,
        validation_alias=AliasChoices("cors_origins", "cors_allow_origins", "CORS_ALLOW_ORIGINS"),
    )

    db_pool_min: int = 1
    db_pool_max: int = 10
    db_statement_timeout_ms: int = 3000

    @computed_field  # type: ignore[misc]
    @property
    def cors_origins(self) -> List[str]:
        """Normalize CORS to a list of strings."""
        v = self.cors_origins_raw
        if v is None:
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        if isinstance(v, list):
            return [s.strip() for s in v if str(s).strip()]
        s = str(v).strip()
        if not s:
            return []
        if s.startswith("["):  # JSON array
            try:
                arr = json.loads(s)
                return [str(x).strip() for x in arr if str(x).strip()]
            except Exception:
                # Fallback to comma split if malformed JSON
                pass
        # Comma-separated or single value
        return [p.strip() for p in s.split(",") if p.strip()]

settings = Settings()
