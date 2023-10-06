from telegram_bot import PropertyBot
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('TOKEN')

if __name__ == "__main__":
    telebot = PropertyBot(TOKEN)
    telebot.start()

