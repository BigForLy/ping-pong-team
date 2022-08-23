from pydantic import BaseSettings
from functools import lru_cache
from typing import List


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str
    kafka_server: str
    kafka_port: int
    kafka_tags: List[str]
    kafka_group_id: str
    router_prefix: str
    customer_tag: str
    producer_message: str

    @property
    def kafka_instance(self):
        return f"{self.kafka_server}:{self.kafka_port}"

    class Config:
        env_file = ".env"
