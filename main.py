from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
import handlers


def main() -> None:
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.log_and_filter_order)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == "__main__":
    main()