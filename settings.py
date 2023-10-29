"""File with settings and configs for the project"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: int
    DB_PORT: int
    DB_HOST: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str

    @property
    def DATABASE_URL_async(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        validate_default=False, env_file='.env', extra="allow")


settings = Settings()
