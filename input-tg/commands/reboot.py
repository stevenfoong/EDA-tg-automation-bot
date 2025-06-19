import json
import uuid
from telegram import Update
from telegram.ext import ContextTypes
from services.rabbitmq_async import publish_to_aws_worker_queue

from services.permissions import is_command_allowed

# Load allowed servers
with open("data/aws-servers.json") as f:
    AWS_SERVER_MAP = json.load(f)

with open("data/ph-servers.json") as f:
    PH_SERVER_MAP = json.load(f)

async def reboot_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    if not is_command_allowed(chat_id, user_id, "reboot_server"):
        return

    # Check if instance parameter is provided
    if not context.args:
        await update.message.reply_text("Please specify the server name. Usage: /reboot <server_name>")
        return

    server_name = context.args[0]

    # Validate the server name
    if server_name not in AWS_SERVER_MAP and server_name not in PH_SERVER_MAP:
        await update.message.reply_text(f"❌ Server '{server_name}' not recognized or not allowed.")
        return

    if server_name in AWS_SERVER_MAP:
        server_info = AWS_SERVER_MAP[server_name]
    elif server_name in PH_SERVER_MAP:
        server_info = PH_SERVER_MAP[server_name]

    # Generate task
    #server_info = SERVER_MAP[server_name]
    #instance_id = server_info["instance_id"]
    #region = server_info["region"]
    task = {
        "command": "reboot server",
        "server_name": server_name,
        "instance_id": server_info["instance_id"],
        "region": server_info["region"],
        "aws_account_id": server_info["aws_account_id"],
        "instance_type": server_info["instance_type"],
        "chat_id": chat_id,
        "user_id": user_id,
        "task_id": str(uuid.uuid4())
    }

    # Publish to RabbitMQ
    await publish_to_aws_worker_queue(task)

    await update.message.reply_text(f"✅ Reboot request for `{server_name}` submitted.\nTask ID: `{task['task_id']}`", parse_mode="Markdown")

