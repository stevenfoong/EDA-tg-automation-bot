import asyncio
from telegram.ext import Application

TOKEN = "111"
CHAT_ID = -222  # or group id (negative number)

async def send_test():
    app = Application.builder().token(TOKEN).build()
    await app.bot.send_message(chat_id=CHAT_ID, text="Test from minimal script")
    await app.shutdown()  # Clean shutdown

asyncio.run(send_test())

