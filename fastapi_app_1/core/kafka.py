from __future__ import annotations
import asyncio
from typing import Any, Callable, Dict
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from core.config import get_settings, Settings
from aiokafka.errors import KafkaTimeoutError, KafkaError
from loguru import logger


def exception_kafka(func: Callable):
    async def _inner(*args, **kwargs):
        try:
            logger.info(f"{kwargs=}")
            return await func(*args, **kwargs)
        except KafkaTimeoutError:
            logger.error(f"KafkaTimeoutError — {args=} — {kwargs=}")
        except KafkaError as e:
            logger.error(f"KafkaError:{e} — {args=} — {kwargs=}")
        except TypeError as e:
            logger.error(f"TypeError:{e} — {args=} — {kwargs=}")

    return _inner


class SingletonMeta(type):
    _instances: Dict[SingletonMeta, Kafka] = {}

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
        self.customer_tag = settings.customer_tag
        self.message = settings.producer_message

    def create_producer(self, settings: Settings):
        loop = asyncio.get_event_loop()
        return AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=settings.kafka_instance,
        )

    def create_aioconsumer(self, settings: Settings):
        loop = asyncio.get_event_loop()
        return AIOKafkaConsumer(
            *settings.kafka_tags,
            bootstrap_servers=settings.kafka_instance,
            loop=loop,
            group_id=settings.kafka_group_id,
        )

    async def consume(self):
        await self.aioconsumer.start()
        try:
            async for msg in self.aioconsumer:
                logger.info(
                    (
                        "consumed: ",
                        msg.topic,
                        msg.partition,
                        msg.offset,
                        msg.key,
                        msg.value,
                        msg.timestamp,
                    )
                )
                await asyncio.sleep(5)
                await self.send(message=self.message.encode())

        finally:
            await self.aioconsumer.stop()

    @exception_kafka
    async def send(self, *, message: bytes):
        await self.aioproducer.send(self.customer_tag, value=message)


def get_kafka_instance():
    return Kafka()
