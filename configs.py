from dotenv import dotenv_values

config = dotenv_values(".env")  # Makes a dict out of the values.

BOT_TOKEN = config["BOT_TOKEN"]
