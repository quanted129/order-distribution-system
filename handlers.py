import logging
import config
import geocoder
import parser
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_order_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat.id
    topic_id = update.message.message_thread_id
    logger.info(f"Received message in chat_id={chat_id}, topic_id={topic_id}")

    if topic_id != config.DELIVERY_TEST_TOPIC_ID:
        return

    parsed_order = await parser.parse_order_from_text(update.message.text)
    if parsed_order is None or not parsed_order.is_valid_order:
        logger.info("Message ignored: not a valid order.")
        return

    if parsed_order.address:
        client = context.bot_data.get("http_client")
        coords = await geocoder.get_coordinates(parsed_order.address, client=client)
        if coords is not None:
            parsed_order.latitude, parsed_order.longitude = coords

    reply = (
        f"Заказ принят в доставку!\n\n"
        f"Магазин: {parsed_order.shop_name}\n"
        f"Адрес: {parsed_order.address}\n"
        f"Интервал: {parsed_order.time_interval}\n"
        f"Координаты: {parsed_order.latitude}, {parsed_order.longitude}"
    )
    await update.message.reply_text(reply)