from pydantic import BaseSettings
from functools import lru_cache
from typing import List


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "fast_api_3"
    kafka_instance: str
    kafka_tags: List[str] = ["mic3"]
    kafka_group_id: str = "mic3"
    router_prefix: str = "/api"

    class Config:
        env_file = ".env"
