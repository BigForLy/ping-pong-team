from pydantic import BaseSettings
from functools import lru_cache
from typing import List


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "fast_api_4"
    kafka_instance: str
    kafka_tags: List[str] = ["mic4"]
    kafka_group_id: str = "mic4"

    class Config:
        env_file = ".env"
