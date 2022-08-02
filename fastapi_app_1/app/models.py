from pydantic import BaseModel


class PingPong(BaseModel):
    app_name: str
    method_name: str
