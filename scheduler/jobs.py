import asyncio
import logging
from youtube.checker import check_for_new_videos
from telegram_bot.notifier import notify

logger = logging.getLogger(__name__)

async def scheduled_check(app):
    loop = asyncio.get_running_loop()
    videos = await loop.run_in_executor(None, check_for_new_videos)

    if videos:
        await notify(app, videos)