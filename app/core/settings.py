from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Chatbot System"
    app_version: str = "0.2.0"

    ai_provider: Literal["openai", "groq", "gemini", "claude"] = "gemini"

    ai_model: str = "gemini-1.5-flash"

    embedding_model: str = "text-embedding-3-small"

    openai_api_key: str | None = Field(default=None, repr=False)
    groq_api_key: str | None = Field(default=None, repr=False)
    gemini_api_key: str | None = Field(default=None, repr=False)
    claude_api_key: str | None = Field(default=None, repr=False)

    vector_backend: Literal["pgvector", "pinecone", "in_memory"] = "in_memory"
    pgvector_dsn: str | None = None
    pinecone_api_key: str | None = Field(default=None, repr=False)
    pinecone_index: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
