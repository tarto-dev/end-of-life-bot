# from dotenv import dotenv_values
import os

# config = dotenv_values(".env")  # Makes a dict out of the values.

# BOT_TOKEN = config["BOT_TOKEN"]
BOT_TOKEN = os.getenv("BOT_TOKEN")
SENTRY_DSN = os.getenv("SENTRY_DSN")
API_URL = os.getenv("API_URL")
