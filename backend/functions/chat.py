from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from telegram.constants import ParseMode
from gemini_client import model
import re
import logging

logger = logging.getLogger("Krishta Bot/chat")

# Define states
CHATTING = 1

chat = model.start_chat(
    enable_automatic_function_calling=True
    )
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
    if not text:
        return "No response generated. Please try again."
        
    # Remove existing formatting if any
    text = text.replace('```', '`')
    
    # Format lists
    text = re.sub(r'^\*\s+', '• ', text, flags=re.MULTILINE)
    
    # Format bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    text = re.sub(r'\*(.+?)\*', r'_\1_', text)
    
    # Escape special characters that aren't part of formatting
    special_chars = ['[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    
    return text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_message = update.message.text
        
        if user_message.lower() == 'bye':
            keyboard = [[InlineKeyboardButton("Start New Chat", callback_data='start_chat')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "_Chat session ended\\!_",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=reply_markup
            )
            logger.info(f"Chat session ended with user {update.effective_user.id}")
            return ConversationHandler.END

        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )

        current_msg = await update.message.reply_text(
            "_Thinking...🤔_",
            parse_mode="Markdown"
        )
        
        logger.info(f"User {update.effective_user.id} asked a question")

        # Get response from Gemini
        response = chat.send_message(user_message)
        logger.info("Response received from Gemini")
                            
        try:
            # Format the response
            formatted_text = format_markdown(response.text)
            
            # Send formatted response
            await current_msg.edit_text(
                formatted_text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            
        except Exception as format_error:
            logger.warning(f"Formatting failed: {format_error}")
            # Fallback to plain text
            await current_msg.edit_text(
                response.text,
            )
        
        logger.info(f"Response sent to user {update.effective_user.id}")
        return CHATTING

    except Exception as e:
        logger.error(f"Error in chat function: {str(e)}", exc_info=True)
        await current_msg.edit_text(
            "_Error: Something went wrong\\. Please try again\\._",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return CHATTING

# Create conversation handler
chat_handler = ConversationHandler(
    entry_points=[CommandHandler("chat", start_chat)],
    states={
        CHATTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
    },
    fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)]
)