from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    auth_secret_key: str
    auth_algorithm: str
    auth_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
