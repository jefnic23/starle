from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str
    API_READ_ACCESS_TOKEN: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
