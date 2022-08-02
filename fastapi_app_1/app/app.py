from fastapi import APIRouter
from fastapi import Depends
from app.models import PingPong

from core.config import Setting, get_setting


router = APIRouter()


@router.get("/ping/", response_model=PingPong)
async def ping(setting: Setting = Depends(get_setting)):
    return PingPong(app_name=setting.app_name, method_name="pong")
