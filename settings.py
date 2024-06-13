from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "footstats"
    mongod_uri: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    MONGO_INITDB_ROOT_PASSWORD: str = ''
    MONGO_INITDB_ROOT_USERNAME: str = ''
    MONGO_INITDB_DATABASE: str = ''

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
