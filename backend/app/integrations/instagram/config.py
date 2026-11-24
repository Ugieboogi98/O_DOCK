from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class InstagramSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    meta_app_id: str = ''
    meta_app_secret: SecretStr = SecretStr('')
    meta_ig_login_config_id: str = ''
    meta_access_token: SecretStr = SecretStr('')
    meta_ig_user_id: str = ''
    meta_graph_api_version: str = ''
    meta_graph_base_url: str = 'https://graph.facebook.com'
    instagram_collection_enabled: bool = False
    instagram_dry_run: bool = True
    instagram_collection_interval_hours: int = Field(default=12, ge=1)
    instagram_collection_page_limit: int = Field(default=1, ge=1, le=3)
    instagram_collection_media_limit: int = Field(default=10, ge=1, le=10)

    @classmethod
    def from_local_env(cls, path=None):
        default = Path(__file__).resolve().parents[4] / '.env'
        return cls(_env_file=path or default, _env_file_encoding='utf-8-sig')
