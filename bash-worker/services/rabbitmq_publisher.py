import aio_pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "pass")

OUTPUT_QUEUE = "output_tg_queue"

async def publish_to_rabbitmq(message: dict):
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
    )
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode()
        ),
        routing_key=OUTPUT_QUEUE,
    )
    await connection.close()

