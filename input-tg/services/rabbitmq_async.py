import os
import aio_pika
import json
import logging
import asyncio

logger = logging.getLogger(__name__)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "pass")

OUTPUT_QUEUE = "output_tg_queue"
BASH_WORKER_QUEUE = "bash_worker_queue"
PH_BASH_WORKER_QUEUE = "ph_bash_worker_queue"
AWS_WORKER_QUEUE = "aws_worker_queue"

async def publish_to_output_queue(task):
    try:
        url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
        connection = await aio_pika.connect_robust(url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(OUTPUT_QUEUE, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(task).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=OUTPUT_QUEUE
            )
            logger.info(f"Diagnostic task published: {task}")
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")

async def publish_to_bash_worker_queue(task):
    try:
        url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
        connection = await aio_pika.connect_robust(url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(BASH_WORKER_QUEUE, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(task).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=BASH_WORKER_QUEUE
            )
            logger.info(f"Diagnostic task published: {task}")
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")

async def publish_to_ph_bash_worker_queue(task):
    try:
        url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
        connection = await aio_pika.connect_robust(url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(PH_BASH_WORKER_QUEUE, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(task).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=PH_BASH_WORKER_QUEUE
            )
            logger.info(f"Diagnostic task published: {task}")
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")

async def publish_to_aws_worker_queue(task):
    try:
        url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
        connection = await aio_pika.connect_robust(url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(AWS_WORKER_QUEUE, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(task).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=AWS_WORKER_QUEUE
            )
            logger.info(f"Reboot server task published: {task}")
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")


# Example usage inside an async function:
# await publish_to_rabbitmq_async({"cmd": "diagnostic"})

