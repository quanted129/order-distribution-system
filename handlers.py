import logging
import geocoder
import parser
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from database import AsyncSessionLocal
from typing import Optional
from models import Shop, Driver, Order

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SHOP_TIMEZONE = timezone(timedelta(hours=3))  # static timezone UTC+3


async def resolve_shop(session: AsyncSession, chat_id: int, topic_id: Optional[int]) -> Optional[int]:
    query = select(Shop.shop_id).where(Shop.telegram_chat_id == chat_id, Shop.telegram_topic_id == topic_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


def parse_time_interval(time_interval: Optional[str]) -> tuple[Optional[datetime], Optional[datetime]]:
    now = datetime.now(SHOP_TIMEZONE)
    if not time_interval: return None, None
    if time_interval.startswith("к "):
        hour, minute = map(int, time_interval[2:].strip().split(':'))
        dt_exact = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return None, dt_exact
    elif '-' in time_interval:
        time_interval_start, time_interval_end = map(str, time_interval.strip().split('-'))
        hour_start, minute_start = map(int, time_interval_start.strip().split(':'))
        hour_end, minute_end = map(int, time_interval_end.strip().split(':'))
        dt_start = now.replace(hour=hour_start, minute=minute_start, second=0, microsecond=0)
        dt_end = now.replace(hour=hour_end, minute=minute_end, second=0, microsecond=0)
        return dt_start, dt_end
    else:
        return None, None


async def handle_order_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat.id
    topic_id = update.message.message_thread_id
    logger.info(f"Received message in chat_id={chat_id}, topic_id={topic_id}")

    async with AsyncSessionLocal() as session:
        shop_id = await resolve_shop(session, chat_id, topic_id)
        if shop_id is None:
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
        else:
            logger.info("Message ignored: no address detected.")
            return

        start_time, end_time = parse_time_interval(parsed_order.time_interval)

        order = Order(
            shop_id=shop_id,
            latitude=parsed_order.latitude,
            longitude=parsed_order.longitude,
            address=parsed_order.address,
            start_time=start_time,
            end_time=end_time,
            item_info=parsed_order.order_contents,
            driver_info=parsed_order.driver_details
        )

        session.add(order)
        await session.commit()

    reply = (
        f"Заказ принят в доставку!\n\n"
        f"Магазин: {parsed_order.shop_name}\n"
        f"Адрес: {parsed_order.address}\n"
        f"Интервал: {parsed_order.time_interval}\n"
        f"Координаты: {parsed_order.latitude}, {parsed_order.longitude}"
    )
    await update.message.reply_text(reply)