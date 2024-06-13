import json
from logging import getLogger

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app import settings

api_logger = getLogger("api")


async def consume_kafka_events():
    """
    Consume events from Kafka
    """
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_SERVER,
    )
    await consumer.start()

    try:
        async for msg in consumer:
            event_data = json.loads(msg.value.decode('utf-8'))
            api_logger.debug(f"Received event from Kafka: {event_data}")
    except KafkaError as e:
        api_logger.error(f"Failed to consume event from Kafka: {e}")
    finally:
        await consumer.stop()


async def send_kafka_event(event_data: dict):
    """
    Send events to Kafka
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER
    )
    await producer.start()

    try:
        value = json.dumps(event_data).encode('utf-8')
        api_logger.debug(f"Sending event to Kafka: {event_data}")
        await producer.send_and_wait(settings.KAFKA_TOPIC, value)

    except KafkaError as e:
        api_logger.error(f"Failed to send event to Kafka: {e}")

    finally:
        await producer.stop()
