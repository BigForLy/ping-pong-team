from fastapi import APIRouter
from fastapi import Depends
from app.models import PingPong

from core.config import Settings, get_settings
from core.kafka import Kafka, get_kafka_instance
from core.const import PONG_MESSAGE


router = APIRouter()


@router.get("/ping/", response_model=PingPong)
async def ping(
    setting: Settings = Depends(get_settings),
    server: Kafka = Depends(get_kafka_instance),
):
    await server.send(message=PONG_MESSAGE)
    return PingPong(app_name=setting.app_name, method_name=PONG_MESSAGE)
