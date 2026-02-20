from telegram.ext import Application, CommandHandler
from logging_config import setup_logging
from config import TELEGRAM_TOKEN, CHECK_INTERVAL_MINUTES
from db.database import init_db
from telegram_bot.handlers import start, unsubscribe, help_command
from scheduler.jobs import scheduled_check

def main():
    setup_logging()
    init_db()

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("help", help_command))

    app.job_queue.run_repeating(
        lambda ctx: scheduled_check(app),
        interval=CHECK_INTERVAL_MINUTES * 60,
        first=5
    )

    app.run_polling()

if __name__ == "__main__":
    main()