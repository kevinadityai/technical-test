from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Info
    APP_ENV: str
    APP_NAME: str
    APP_VERSION: str

    # Qdrant
    QDRANT_URL: str
    COLLECTION_NAME: str
    
    model_config = SettingsConfigDict(env_file=".env")

env = Settings()
