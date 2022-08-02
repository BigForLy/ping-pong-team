from pydantic import BaseSettings
from functools import lru_cache


@lru_cache
def get_setting():
    return Setting()


class Setting(BaseSettings):
    app_name: str = "fast_api_1"
