from fastapi import APIRouter
from fastapi import Depends
from app.models import PingPong

from core.config import Settings, get_settings


router = APIRouter()


@router.get("/ping/", response_model=PingPong)
async def ping(setting: Settings = Depends(get_settings)):
    return PingPong(app_name=setting.app_name, method_name="pong")
