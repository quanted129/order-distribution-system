import logging
import json

import config
from telegram import Update
from telegram.ext import ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def log_and_filter_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text: return

    message_text = update.message.text
    topic_id = update.message.message_thread_id

    print(json.dumps(update.to_dict(), indent=2))

    if topic_id == config.DELIVERY_TEST_TOPIC_ID:
        await update.message.reply_text(
            "Order received!",
            read_timeout=20,
            write_timeout=20
        )


async def handle_order_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Orchestrates the order intake pipeline:
    1. Validates that the message has text and belongs to the designated DELIVERY_TEST_TOPIC_ID.
    2. Passes the raw text to parser.parse_order_from_text().
    3. If the parsed order is not valid (chitchat/dialogue), logs and ignores it.
    4. If valid, retrieves the shared httpx.AsyncClient from context.bot_data (if available).
    5. Calls geocoder.get_coordinates() to populate parsed_order.latitude and longitude.
    6. Sends a formatted reply back to the Telegram chat showing the extracted fields and coords.

    Inputs:
        update: The Telegram Update object containing the message.
        context: The Telegram context (context.bot_data holds shared state).
    """
    # 1. Guard clause: Ensure message exists and has text
    # 2. Check topic ID (message_thread_id)
    # 3. Call parser
    # 4. If not is_valid_order: log and exit
    # 5. Geocode the address
    # 6. Reply to Telegram with confirmation
    pass