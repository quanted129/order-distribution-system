from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters
import httpx
import config
import handlers


async def post_init_handler(application: Application) -> None:
    client = httpx.AsyncClient(timeout=10)
    application.bot_data["http_client"] = client


async def post_stop_handler(application: Application) -> None:
    client = application.bot_data["http_client"]
    await client.aclose()


def main() -> None:
    application = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .post_init(post_init_handler)
        .post_stop(post_stop_handler)
        .concurrent_updates(True)
        .build()
    )
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.handle_order_message)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == "__main__":
    main()