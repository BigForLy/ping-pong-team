from fastapi import FastAPI
from core.config import get_settings
from core.const import SHUTDOWN_EVENT, STARTUP_EVENT
from core.events import create_stop_app_handler, create_start_app_handler
from routes import router as router_api


def get_application() -> FastAPI:
    application = FastAPI()
    settings = get_settings()

    application.include_router(router_api, prefix=settings.router_prefix)

    application.add_event_handler(STARTUP_EVENT, create_start_app_handler)
    application.add_event_handler(SHUTDOWN_EVENT, create_stop_app_handler)

    return application


app: FastAPI = get_application()
