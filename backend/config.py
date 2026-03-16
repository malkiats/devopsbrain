from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve .env location: prefer project-root .env (used by Vercel/api/index.py),
# fall back to the backend-directory .env for pure-backend local development.
_backend_dir = Path(__file__).resolve().parent
_root_env = _backend_dir.parent / ".env"
_backend_env = _backend_dir / ".env"
_env_file = str(_root_env) if _root_env.exists() else str(_backend_env)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "DevOpsBrain API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    # AI provider — defaults to openai when OPENAI_API_KEY is present.
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str | None = None         # legacy alias kept for backward compat
    openai_api_key: str | None = None      # preferred: set via OPENAI_API_KEY env var

    # Database — POSTGRES_URL (Supabase/Vercel style) takes precedence over POSTGRES_DSN.
    postgres_dsn: str = Field(default="postgresql://postgres:postgres@localhost:5432/devopsbrain")
    postgres_url: str | None = None

    redis_url: str = Field(default="redis://localhost:6379/0")

    @property
    def effective_openai_key(self) -> str | None:
        return self.openai_api_key or self.llm_api_key

    @property
    def effective_postgres_url(self) -> str:
        return self.postgres_url or self.postgres_dsn

    model_config = SettingsConfigDict(env_file=_env_file, env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
