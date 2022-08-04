from fastapi import FastAPI
from core.config import get_settings
from core.const import SHUTDOWN_EVENT, STARTUP_EVENT
from routes import router as router_api
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio


class MyFastAPI(FastAPI):
    def initialize_kafka(self):
        settings = get_settings()

        loop = asyncio.get_event_loop()
        self.aioproducer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=settings.kafka_instance,
            client_id=settings.app_name,
        )
        self.aioconsumer = AIOKafkaConsumer(
            *settings.kafka_tags,
            bootstrap_servers=settings.kafka_instance,
            loop=loop,
            client_id=settings.app_name,
            group_id=settings.kafka_group_id
        )

    async def consume_start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.consume())

    async def consume(self):
        await self.aioconsumer.start()
        try:
            async for msg in self.aioconsumer:
                print(
                    "consumed: ",
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
                await asyncio.sleep(5)
                await app.aioproducer.send("mic3", key=b"mic3", value=b"ping")

        finally:
            await self.aioconsumer.stop()

    async def startup_event(self):
        self.initialize_kafka()
        await self.aioproducer.start()
        await self.consume_start()

    async def shutdown_event(self):
        await self.aioproducer.stop()
        await self.aioconsumer.stop()


def get_application() -> MyFastAPI:
    application = MyFastAPI()

    application.include_router(router_api, prefix="/api")

    application.add_event_handler(STARTUP_EVENT, application.startup_event)
    application.add_event_handler(SHUTDOWN_EVENT, application.shutdown_event)

    return application


app: MyFastAPI = get_application()
