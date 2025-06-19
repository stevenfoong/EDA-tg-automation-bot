import uuid
from telegram import Update
from telegram.ext import ContextTypes  # for PTB v20+
from services.rabbitmq_async import publish_to_output_queue
from services.rabbitmq_async import publish_to_bash_worker_queue
from services.rabbitmq_async import publish_to_ph_bash_worker_queue

from services.permissions import is_command_allowed

async def diagnostic_tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    diagnostic_id = str(uuid.uuid4())

    if not is_command_allowed(chat_id, user_id, "diag_tg"):
        return

    task = {
        "diagnostic_id": diagnostic_id,
        "chat_id": chat_id,
        "user_id": user_id,
        "command": "diagnostic_tg"
    }

    # ASYNC call!
    await publish_to_output_queue(task)
    await update.message.reply_text(
        f"Diagnostic TG request sent. Please wait for the output bot's response.\nDiagnostic ID: {diagnostic_id}"
    )

async def diagnostic_ind_cloud_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    diagnostic_id = str(uuid.uuid4())

    if not is_command_allowed(chat_id, user_id, "diag_ind_cloud_proxy"):
        return

    servers = {
        "ind01.copaybo.net": "172.26.2.162",
        "ind02.copaybo.net": "172.26.15.193",
        "ind03.copaybo.net": "43.205.145.252"
    }


    for server_name, server_ip in servers.items():
        task = {
            "diagnostic_id": diagnostic_id,
            "chat_id": chat_id,
            "user_id": user_id,
            "task": "diagnostic_cloud_proxy",
            "target_server": server_name,
            "target_ip": server_ip
        }

        # ASYNC call to send each task
        await publish_to_bash_worker_queue(task)

    server_list = ', '.join(servers.keys())
    await update.message.reply_text(
        f"Diagnostic ind cloud proxy requests sent for the following servers: {server_list}.\n"
        f"Please wait for the diagnostic result.\nDiagnostic ID: {diagnostic_id}"
    )

async def diagnostic_ind_ph_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    diagnostic_id = str(uuid.uuid4())

    if not is_command_allowed(chat_id, user_id, "diag_ind_ph_proxy"):
        return

    servers = {
        "proxy-ind-01.local": "10.26.14.251",
        "proxy-ind-02.local": "10.26.14.253",
        "proxy-ind-03.local": "10.26.14.254"
    }


    for server_name, server_ip in servers.items():
        task = {
            "diagnostic_id": diagnostic_id,
            "chat_id": chat_id,
            "user_id": user_id,
            "task": "diagnostic_local_proxy",
            "target_server": server_name,
            "target_ip": server_ip
        }

        # ASYNC call to send each task
        await publish_to_ph_bash_worker_queue(task)

    server_list = ', '.join(servers.keys())
    await update.message.reply_text(
        f"Diagnostic ind local proxy requests sent for the following servers: {server_list}.\n"
        f"Please wait for the diagnostic result.\nDiagnostic ID: {diagnostic_id}"
    )

