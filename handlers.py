from telegram import Update
from telegram.ext import Application
import config
from basic_handlers import basic_handlers
from admin_handlers import admin_handlers, send_startup_message
from question_handlers import question_handlers

def main():
    app = Application.builder().token(config.BOT_TOKEN).build()
    for handler in basic_handlers + admin_handlers + question_handlers:
        app.add_handler(handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES, timeout=60)
    app.job_queue.run_once(lambda _: app.create_task(send_startup_message(app)), 1)

if __name__ == '__main__':
    main()
