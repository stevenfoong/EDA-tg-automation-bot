import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
