from telegram_bot import PropertyBot
TOKEN ="XYZ"# get token from command-line


if __name__ == "__main__":
    telebot = PropertyBot(TOKEN)
    telebot.start()

