import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
YANDEX_API_KEY: str = os.environ["YANDEX_API_KEY"]
YANDEX_GEOCODER_URL: str = os.environ["YANDEX_GEOCODER_URL"]
OSRM_TABLE_URL: str = os.environ["OSRM_TABLE_URL"]
GEMINI_API_KEY: str = os.environ["GEMINI_API_KEY"]
DB_HOST: str = os.environ["DB_HOST"]
DB_PORT: str = os.environ["DB_PORT"]
DB_NAME: str = os.environ["DB_NAME"]
DB_USER: str = os.environ["DB_USER"]
DB_PASSWORD: str = os.environ["DB_PASSWORD"]

DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"