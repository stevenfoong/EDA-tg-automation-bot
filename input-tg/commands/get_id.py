import logging

from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

async def get_id(update: Update, context: CallbackContext) -> None:
    # Check if message is available
    if update.message is None:
        return  # If message is None, return early

    chat = update.message.chat

    logger.info(
        f"User {update.message.from_user.id} ({update.message.from_user.username}) used /get_id in chat {chat.id} (type: {chat.type})"
    )

    # If it's a group chat, return the group ID
    if chat.type in ['group', 'supergroup']:
        chat_id = chat.id
        await update.message.reply_text(f"This is a group. Group ID: {chat_id}")
    # If it's a direct message, return the user ID
    else:
        user_id = update.message.from_user.id
        await update.message.reply_text(f"This is a direct message. Your User ID: {user_id}")

