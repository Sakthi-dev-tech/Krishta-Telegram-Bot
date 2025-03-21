from telegram import ForceReply, Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger("Krishta Bot/start")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    logger.info("User started bot")
    
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )