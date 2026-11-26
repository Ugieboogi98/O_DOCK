from functools import lru_cache
from pathlib import Path
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / '.env', extra="ignore")
    database_url: str = (
        "postgresql+psycopg://figure:figure_local@localhost:5432/figure_archive"
    )
    data_dir: Path = PROJECT_ROOT / 'data'
    media_dir: Path = PROJECT_ROOT / 'media'
    # Writable, never served: pipeline reports, semantic stage caches, raw event snapshots.
    private_dir: Path = PROJECT_ROOT / 'data' / 'private'
    semantic_report_dir: Path = PROJECT_ROOT / 'data' / 'private' / 'semantics' / 'split_queue_20261117'
    chroma_host: str = ""
    chroma_port: int = 8000
    chroma_path: str = str(PROJECT_ROOT / 'data/chroma')
    embedding_provider: str = "hash"
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: str = ""
    embedding_base_url: str = "https://api.openai.com/v1"
    auto_translate_names: bool = False
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4.1-mini"
    llm_api_mode: str = "chat"  # 'responses' for GMS models documented with /responses
    semantic_provider: str = 'remote'
    semantic_model: str = 'qwen3:8b'
    semantic_base_url: str = 'http://host.docker.internal:11434'
    semantic_timeout: int = 240
    semantic_num_ctx: int = 32768
    semantic_translation_model: str = 'qwen3:8b'
    semantic_classification_model: str = 'qwen3:1.7b'
    semantic_reference_enrichment: bool = False
    search_api_key: str = ""
    admin_token: str = ""
    auth_cookie_secure: bool = False  # Enable for HTTPS deployments.
    cors_origins: str = "http://localhost:5173,http://localhost:8080"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    fetch_k: int = 20
    retrieval_mode: str = "similarity"
    price_cache_minutes: int = 60
    price_max_age_hours: int = 168
    collection_delay_seconds: float = 2.0
    request_timeout: int = 20
    user_agent: str = "O_DOCKResearch/1.0 (+local educational project)"

    @model_validator(mode="after")
    def validate_settings(self):
        if self.semantic_provider not in ('remote', 'ollama'):
            raise ValueError('semantic_provider must be remote or ollama')
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        if self.top_k < 1 or self.fetch_k < self.top_k:
            raise ValueError("Invalid top_k/fetch_k")
        if self.embedding_provider not in ("hash", "openai"):
            raise ValueError("embedding_provider must be hash or openai")
        return self


@lru_cache
def get_settings():
    return Settings()
