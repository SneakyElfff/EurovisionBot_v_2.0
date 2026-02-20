import logging
from db.subscribers import get_subscribers

logger = logging.getLogger(__name__)

async def notify(app, videos):
    for chat_id in get_subscribers():
        for video in videos:
            try:
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=f"🎬 {video['title']}\n{video['url']}"
                )
            except Exception:
                logger.exception("Failed to notify %s", chat_id)