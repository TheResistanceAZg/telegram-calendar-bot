from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from config.settings import TELEGRAM_TOKEN
from bot.handlers import check_availability

def main():
    """Starts the bot using the modular structure."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Trigger the bot using regular text messages that are NOT commands
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_availability))

    print("Bot is listening for questions...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()