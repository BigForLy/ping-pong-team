from __future__ import annotations
import asyncio
from typing import Any, Dict
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from core.config import get_settings, Settings


class SingletonMeta(type):
    _instances: Dict[Any, Any] = {}  # TODO

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self not in self._instances:
            instance = super().__call__(*args, **kwds)
            self._instances[self] = instance
        return self._instances[self]


class Kafka(metaclass=SingletonMeta):
    def __init__(self) -> None:
        settings = get_settings()
        self.aioproducer = self.create_producer(settings)
        self.aioconsumer = self.create_aioconsumer(settings)

    def create_producer(self, settings: Settings):
        loop = asyncio.get_event_loop()
        return AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=settings.kafka_instance,
            client_id=settings.app_name,
        )

    def create_aioconsumer(self, settings: Settings):
        loop = asyncio.get_event_loop()
        return AIOKafkaConsumer(
            *settings.kafka_tags,
            bootstrap_servers=settings.kafka_instance,
            loop=loop,
            client_id=settings.app_name,
            group_id=settings.kafka_group_id,
        )

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
                await self.send(message=b"pong")

        finally:
            await self.aioconsumer.stop()

    async def send(self, *, message: bytes):
        try:
            # TODO: EDIT EXCEPTIOPN
            await self.aioproducer.send("mic4", key=b"foo", value=message)
        except Exception as e:
            await self.aioproducer.stop()
            raise e


def get_kafka_instance():
    return Kafka()
