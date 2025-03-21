from telegram.ext import ApplicationBuilder, CommandHandler
from functions.start import start
from functions.chat import chat_handler
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s %(levelname)s -> %(message)s",
    handlers=[
        logging.FileHandler('bot.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# Create logger for this module
logger = logging.getLogger("Krishta Bot")

API_KEY = os.getenv("KRISHTA_API_KEY")

def main() -> None:
    try:
        # Start the bot
        logger.info("Starting bot...")
        # Create application
        application = ApplicationBuilder().token(API_KEY).build()
        logger.info("Bot built successfully")

        application.add_handler(CommandHandler("start", start))
        application.add_handler(chat_handler)
        logger.info("Handlers added successfully")

        application.run_polling(poll_interval=3)
        logger.info("Bot started running successfully")
    except Exception as e:
        logger.error(f"An error occurred while initialising bot: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()