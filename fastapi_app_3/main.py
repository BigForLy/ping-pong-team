from fastapi import FastAPI
from core.const import SHUTDOWN_EVENT, STARTUP_EVENT
from core.events import shutdown_event, startup_event
from routes import router as router_api


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(router_api, prefix="/api")  # TODO

    application.add_event_handler(STARTUP_EVENT, startup_event)
    application.add_event_handler(SHUTDOWN_EVENT, shutdown_event)

    return application


app: FastAPI = get_application()
