from fastapi import APIRouter
from fastapi import Depends
from app.models import PingPong

from core.config import Settings, get_settings
from core.kafka import Kafka, get_kafka_instance


router = APIRouter()


@router.get("/ping/", response_model=PingPong)
async def ping(
    setting: Settings = Depends(get_settings),
    server: Kafka = Depends(get_kafka_instance),
):
    try:
        #  TODO
        await server.aioproducer.send("mic3", key=b"foo", value=b"bar")
        return PingPong(app_name=setting.app_name, method_name="pong")
    except Exception as e:
        await server.aioproducer.stop()
        raise e
