# Automated order distribution system

A logistics automation tool designed to distribute orders efficiently in real-time using a dynamic vehicle routing backend system built in Python. Designed for multi-shop partner networks and live courier fleets.

## Key Features

- **Automated Telegram order intake**: Listens to messages in dedicated groups/topics and allows for asynchronous update processing so no shop gets left without service during periods of high demand.
- **AI-Powered text parsing**: Uses the Google GenAI SDK with structured output to extract addresses, time windows, payment details, and courier instructions from unstructured Telegram messages to make the user experience effortless.
- **Yandex geocoding**: Resolves street addresses into exact GPS coordinates using the Yandex Geocoder API. This allows for pinpoint precision in the CIS region and enables perfect ETA delivery time accuracy.
- **Data persistence**: Stores partner shop details, courier information, and validated orders in PostgreSQL. Supports database migrations using Alembic.
- **Dynamic real-time routing (WIP)**.
- **Admin API and smart dashboards (WIP)**.

## Tech Stack

- **Language**: Python 3.14+
- **Environment & dependency manager**: `uv`
- **Database**: PostgreSQL, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`
- **Bot interface**: `python-telegram-bot`
- **Generative AI and structured output**: `google-genai`, `pydantic`
- **External APIs**: Yandex Geocoder, OSRM (`httpx`)

## Installation & Setup

### Prerequisites
- [Python 3.14+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) package manager
- [PostgreSQL](https://www.postgresql.org/download/) local database
- External API keys:
  - Telegram Bot Token (get one from [`@BotFather`](https://telegram.me/BotFather))
  - Google Gemini API Key (create one in [`Google AI Studio`](https://aistudio.google.com/api-keys))
  - Yandex Geocoder API Key (create one in your [`Yandex Maps API account`](https://yandex.ru/maps-api/console))

### 1. Clone the repository and sync dependencies
```bash
git clone https://github.com/quanted129/order-distribution-system
cd order-distribution-system
uv sync
```

### 2. Configure environment variables
Create a `.env` file in the project root and fill out all necessary fields.  
*Note: Use the `.env.example` file as reference for what your `.env` should contain!*

### 3. Run database migrations

Make sure your PostgreSQL database is created, then apply the schema migrations:
```bash
uv run alembic upgrade head
```

### 4. Launch the bot
```bash
uv run python main.py
```