import aio_pika
import os
import logging
import json
from aio_pika import connect_robust

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "pass")

BASH_WORKER_QUEUE = "bash_worker_queue"

async def consume_tasks(callback):

    amqp_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"

    logging.info(f"Connecting to RabbitMQ: {amqp_url}")
    connection = await connect_robust(amqp_url)
    logging.info("Connected! Opening channel...")
    channel = await connection.channel()
    logging.info("Channel opened!")
    bash_worker_queue = await channel.declare_queue(BASH_WORKER_QUEUE, durable=True)
    logging.info("Declared bash_worker_queue!")

    queue = await channel.declare_queue(BASH_WORKER_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    task = json.loads(message.body.decode())
                    logging.info(f"Received task: {task}")
                    payload = message.body.decode()
                    await callback(payload)
                except Exception as e:
                    logging.error(f"Failed to process message: {e}")


