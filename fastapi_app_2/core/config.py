from pydantic import BaseSettings
from functools import lru_cache
from typing import List


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "fast_api_2"
    kafka_server: str
    kafka_port: int
    kafka_tags: List[str] = ["mic2"]
    kafka_group_id: str = "mic2"
    router_prefix: str = "/api"

    @property
    def kafka_instance(self):
        return f"{self.kafka_server}:{self.kafka_port}"

    class Config:
        env_file = ".env"
