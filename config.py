import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env.txt")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_IDS = [ADMIN_ID]

REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "").strip()

PREMIUM_PRICE = os.getenv("PREMIUM_PRICE", "99000")

CLICK_INFO = os.getenv("CLICK_INFO", "")
PAYME_INFO = os.getenv("PAYME_INFO", "")
UZUM_INFO = os.getenv("UZUM_INFO", "")

CONTACT = os.getenv("CONTACT", "@dilmurodbe_05")
CHAT_LINK = os.getenv("CHAT_LINK", "")

DATABASE_PATH = str(BASE_DIR / "bot.db")
