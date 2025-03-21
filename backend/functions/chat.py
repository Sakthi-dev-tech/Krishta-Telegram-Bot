from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from telegram.constants import ParseMode
import re
from gemini_client import client
import logging

logger = logging.getLogger("Krishta Bot/chat")

# Define states
CHATTING = 1
chat = client.chats.create(model="gemini-2.0-flash")

async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the chat session"""
    await update.message.reply_text(
        "Chat session started! You can chat with me now.\n"
        "Send 'bye' to end the conversation."
    )
    logger.info(msg=f"Chat session started with user {update.effective_user.id}")
    return CHATTING

def format_markdown(text: str) -> str:
    """Format text for Telegram Markdown"""
    # Remove existing formatting if any
    text = text.replace('```', '`')
    
    # Format lists
    text = re.sub(r'^\*\s+', '• ', text, flags=re.MULTILINE)  # Convert * lists to •
    
    # Format bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)  # Convert **text** to *text*
    text = re.sub(r'\*(.+?)\*', r'_\1_', text)      # Convert *text* to _text_
    
    # Escape special characters that aren't part of formatting
    special_chars = ['[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    
    return text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_message = update.message.text
        
        if user_message.lower() == 'bye':
            await update.message.reply_text(
                "_Chat session ended\\! Feel free to start a new chat with /chat_",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            logger.info(f"Chat session ended with user {update.effective_user.id}")
            return ConversationHandler.END

        logger.info(f"User {update.effective_user.id} asked: {user_message}")

        # Send initial message
        initial_message = await update.message.reply_text(
            "_🤔 Thinking\\.\\.\\.\\._",
            parse_mode=ParseMode.MARKDOWN_V2
        )

        # Get response from Gemini
        response = chat.send_message(user_message)
        logger.info("Response received from Gemini")
        
        try:
            # Format the response with Markdown
            formatted_text = format_markdown(response.text)
            
            # Try sending with markdown
            await initial_message.edit_text(
                formatted_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as edit_error:
            # If markdown fails, try sending without formatting
            logger.warning(f"Failed to parse markdown: {edit_error}")
            await initial_message.edit_text(response.text)
        
        logger.info(f"Response sent to user {update.effective_user.id}")
        return CHATTING

    except Exception as e:
        logger.error(f"Error in chat function: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "_Sorry, I encountered an error\\. Please try again later\\._",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return ConversationHandler.END

# Create conversation handler
chat_handler = ConversationHandler(
    entry_points=[CommandHandler("chat", start_chat)],
    states={
        CHATTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)]
    },
    fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)]
)