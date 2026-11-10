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
from models import Shop, Order

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
    if not time_interval: return None, None
    now = datetime.now(SHOP_TIMEZONE)
    base_date = now + timedelta(days=1) if now.hour >= 21 else now

    def to_dt(hh_mm: str) -> datetime:
        hour, minute = map(int, hh_mm.strip().split(':'))
        return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    try:
        if time_interval.startswith("к "):
            dt_exact = to_dt(time_interval[2:])
            if dt_exact <= now:
                dt_exact += timedelta(days=1)
            return None, dt_exact

        if '-' in time_interval:
            start_str, end_str = time_interval.split('-')
            dt_start, dt_end = to_dt(start_str), to_dt(end_str)
            if dt_end <= now:
                dt_start += timedelta(days=1)
                dt_end += timedelta(days=1)
            return dt_start, dt_end

        return None, None
    except ValueError:
        logger.warning("Could not parse time_interval: %s", time_interval)
        return None, None


async def handle_order_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.message.chat.id
    topic_id = update.message.message_thread_id
    # logger.info("Received message in chat_id=%s, topic_id=%s", chat_id, topic_id)
    # use this to define new shops in the database
    # TODO: shop adding instructions

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
        driver_info='\n'.join(filter(None, [parsed_order.driver_details, parsed_order.payment_status])) or None
    )

    async with AsyncSessionLocal() as session:
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