from fastapi import FastAPI
from core.config import get_settings
from core.const import SHUTDOWN_EVENT, STARTUP_EVENT
from core.events import shutdown_event, startup_event
from routes import router as router_api


def get_application() -> FastAPI:
    application = FastAPI()
    settings = get_settings()

    application.include_router(router_api, prefix=settings.router_prefix)

    application.add_event_handler(STARTUP_EVENT, startup_event)
    application.add_event_handler(SHUTDOWN_EVENT, shutdown_event)

    return application


app: FastAPI = get_application()
