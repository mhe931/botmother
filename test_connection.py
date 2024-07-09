import config
from telegram import Bot

def test_connection():
    bot = Bot(token=config.BOT_TOKEN)
    try:
        print(bot.get_me())
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
