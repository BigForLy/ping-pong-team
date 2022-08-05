import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from core.config import get_settings, Settings


class Kafka:
    _instance = None

    def __init__(self) -> None:
        settings = get_settings()
        self.aioproducer = self.create_producer(settings)
        self.aioconsumer = self.create_aioconsumer(settings)
        Kafka._instance = self

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
                await self.aioproducer.send("mic4", key=b"mic4", value=b"pong")

        finally:
            await self.aioconsumer.stop()


def get_kafka_instance():
    if Kafka._instance:
        return Kafka._instance
    return Kafka()
