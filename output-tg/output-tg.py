import os
import json
import logging
import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from telegram.ext import Application
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "pass")
OUTPUT_QUEUE = "output_tg_queue"

async def on_message(application, message: IncomingMessage):
    async with message.process():  # auto ack after block
        try:
            body = message.body.decode()
            logger.info(f"Received body from queue: {body}")
            task = json.loads(body)
            chat_id = task.get("chat_id")
            diagnostic_id = task.get("diagnostic_id")
            command = task.get("command")
            message = task.get("message")
            logger.info(f"Using chat_id: {chat_id}, diagnostic_id: {diagnostic_id}")

            if chat_id and (command=="diagnostic_tg"):
                text = f"✅ Diagnostic TG check successful!\nDiagnostic ID: {diagnostic_id}."
                await application.bot.send_message(chat_id=int(chat_id), text=text)
                logger.info(f"Sent diagnostic reply to chat {chat_id}")
                        
            elif chat_id and (command=="diagnostic_cloud_proxy"):
                text = f"✅ Diagnostic TG check successful!\nDiagnostic ID: {diagnostic_id}."
                await application.bot.send_message(chat_id=int(chat_id), text=text)
                logger.info(f"Sent diagnostic reply to chat {chat_id}")

            elif chat_id and diagnostic_id and message:
                text = f"Diagnostic ID: {diagnostic_id}\n{message}"
                await application.bot.send_message(chat_id=int(chat_id), text=text)
                logger.info(f"Sent message to chat {chat_id}")

            elif chat_id and message:
                await application.bot.send_message(chat_id=int(chat_id), text=message)
                logger.info(f"Sent message to chat {chat_id}")

            else:
                logger.warning("Invalid diagnostic task: missing chat_id or diagnostic_id")
        except Exception as e:
            logger.error(f"Error handling diagnostic message: {e}")

async def main():
    # Telegram app (no polling needed for output bot)
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Start application (background initialization)
    await application.initialize()
    # Set up aio-pika connection
    amqp_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"
    connection = await connect_robust(amqp_url)
    channel = await connection.channel()
    # Declare queue
    queue = await channel.declare_queue(OUTPUT_QUEUE, durable=True)
    logger.info(f"Waiting for messages on {OUTPUT_QUEUE} ...")
    # Start consuming
    await queue.consume(lambda message: on_message(application, message))
    # Keep running forever
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

