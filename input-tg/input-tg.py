import logging

from sys import stdout

from telegram.ext import Application, CommandHandler

from commands.get_id import get_id
from commands.help import help_command

from commands.diagnostic import diagnostic_tg
from commands.diagnostic import diagnostic_ind_cloud_proxy
from commands.diagnostic import diagnostic_ind_ph_proxy

from commands.reboot import reboot_server

from config import TELEGRAM_BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():

    # Create an Application instance
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # register_help_command(app)

    # Add command handler for /get_id
    application.add_handler(CommandHandler("get_id", get_id))

    application.add_handler(CommandHandler("diag_tg", diagnostic_tg))
    application.add_handler(CommandHandler("diag_ind_cloud_proxy", diagnostic_ind_cloud_proxy))
    application.add_handler(CommandHandler("diag_ind_ph_proxy", diagnostic_ind_ph_proxy))

    application.add_handler(CommandHandler("reboot_server", reboot_server))

    application.add_handler(CommandHandler("help", help_command))



    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

