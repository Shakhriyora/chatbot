from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    base_url: str
    model: str
    embedding_model: str
    embedding_url: str
    timeout: float = 60.0


settings = Settings()
