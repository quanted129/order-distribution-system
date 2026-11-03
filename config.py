import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
YANDEX_API_KEY : str = os.environ["YANDEX_API_KEY"]
YANDEX_GEOCODER_URL: str = os.environ["YANDEX_GEOCODER_URL"]
DELIVERY_TEST_TOPIC_ID: int = int(os.environ["DELIVERY_TEST_TOPIC_ID"])
GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]