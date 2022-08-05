import asyncio

from core.kafka import get_kafka_instance


async def startup_event():
    kafka_server = get_kafka_instance()
    await kafka_server.aioproducer.start()
    loop = asyncio.get_event_loop()
    loop.create_task(kafka_server.consume())


async def shutdown_event():
    kafka_server = get_kafka_instance()
    await kafka_server.aioproducer.stop()
    await kafka_server.aioconsumer.stop()
