import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
import asyncio
from db.subscribers import add_subscriber, remove_subscriber
from youtube.checker import get_today_videos

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_subscriber(update.effective_chat.id)
    logger.info("New subscriber: %s", update.effective_chat.id)
    await update.message.reply_text('Subscribed! You\'ll get notifications for new videos.')

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remove_subscriber(update.effective_chat.id)
    logger.info("Unsubscribed: %s", update.effective_chat.id)
    await update.message.reply_text('Unsubscribed successfully.')

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺 Gathering today's recap...")

    loop = asyncio.get_running_loop()
    videos = await loop.run_in_executor(None, get_today_videos)

    if not videos:
        await update.message.reply_text(
            "No one presented anything today."
        )
        return

    text = "📅 Entries from today:\n\n"
    for video in videos:
        text += f"• {video['title']}\n{video['url']}\n\n"

    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Commands:\n/start - Subscribe\n/unsubscribe - Unsubscribe\n/help - Show this message')
