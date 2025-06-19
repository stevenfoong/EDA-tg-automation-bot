# commands/help_command.py

import logging

from telegram import Update
from telegram.ext import CallbackContext

#from services.permissions import is_command_allowed
from services.permissions import get_allowed_commands

logger = logging.getLogger(__name__)

HELP_TEXT = """
Available commands:
/help - Show this help message
/get_id - Retrieve your personal id or group id
/diagnostic - Run diagnostic check
/echo <text> - Echo back your message
"""

async def help_command(update: Update, context: CallbackContext) -> None:
    # Check if message is available
    if update.message is None:
        return  # If message is None, return early

    chat = update.message.chat
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    allowed_cmds = get_allowed_commands(chat_id, user_id)

    if not allowed_cmds:
        await update.message.reply_text("You have no permissions to use any commands.")
        return

#    if not is_command_allowed(chat.id, chat.id, "help"):
#        return

    logger.info(
        f"User {update.message.from_user.id} ({update.message.from_user.username}) used /help in chat {chat.id} (type: {chat.type})"
    )

    cmd_list = "\n".join([f"/{cmd}" for cmd in allowed_cmds])
    await update.message.reply_text(f"Available commands:\n{cmd_list}")

#    await update.message.reply_text(HELP_TEXT)

