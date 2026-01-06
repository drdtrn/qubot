import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import asyncio
import time
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN") 
BOTUSERNAME: Final = "@dm_daily_bot"
API_URL = "https://rpc.qubic.org/v1/latest-stats"

# Logger ------------------------------------------------------------
LOG_PATH = os.getenv("PATH")

logger = logging.getLogger("dmprice_bot")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_PATH,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# End Logger -----------------------------------------------------------

CACHE_TTL = 30

_cached_text = None
_cached_at = 0.0
_cache_lock = asyncio.Lock()

async def get_qubic_data():
    global _cached_text, _cached_at
    now = time.time()

    # Double-check pattern
    if _cached_text and (now - _cached_at) < CACHE_TTL:
        return _cached_text

    async with _cache_lock:
        # Re-check after acquiring lock
        now = time.time()
        if _cached_text and (now - _cached_at) < CACHE_TTL:
            return _cached_text

        timeout = aiohttp.ClientTimeout(total=5)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(API_URL) as response:
                    payload = await response.json()

            qubic_info = payload["data"]
            # Formatting (kept your logic)
            price = f"Çmimi momental i Qubic: ${qubic_info['price']:.9f}"
            addresses = f"Numri total i Adresave të QubicWallet: {int(qubic_info['activeAddresses']):,}"
            m_c = f"MarketCap: ${int(qubic_info['marketCap']):,}"
            burned = int(qubic_info['burnedQus'])
            burned_value = burned * qubic_info['price']
            burned_text = f"Sasia e Qubic-ave të djegur: {burned:,} (${burned_value:,.3f})"
            epoka = f"Epoka: {qubic_info['epoch']}"

            text = f"{price}\n{addresses}\n{m_c}\n{burned_text}\n{epoka}"

            _cached_text = text
            _cached_at = time.time()
            return text
        except Exception as e:
            logger.error(f"API Fetch Error: {e}")
            return _cached_text or "Error fetching data."

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    logger.info(
        "/dmprice | "
        f"user_id={user.id if user else 'N/A'} | "
        f"username={user.username if user and user.username else 'N/A'} | "
        f"chat_id={chat.id if chat else 'N/A'} | "
        f"type={chat.type if chat else 'N/A'}"
    )

    text = await get_qubic_data()
    await update.message.reply_text(text)

async def background_cache_refresh(context: ContextTypes.DEFAULT_TYPE):
    """Refreshes cache every 30s. No deadlock here because we just call the main func."""
    while True:
        await get_qubic_data() # This handles its own locking internally
        await asyncio.sleep(CACHE_TTL)

async def post_init(application: Application):
    """This starts the background task correctly within the bot's loop."""
    asyncio.create_task(background_cache_refresh(None))

if __name__ == "__main__":
    # Use post_init to start your background loop
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("dmprice", start_command))

    app.run_polling()
