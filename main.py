import os
import asyncio

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application
)

from config import BOT_TOKEN
from database import init_db

from handlers.ai_teacher import router as ai_teacher_router
from handlers.letters import router as letters_router
from handlers.daily_grammar import router as daily_grammar_router
from handlers.admin_daily_grammar import (
    router as admin_daily_grammar_router
)
from handlers.grammar import router as grammar_router
from handlers.podcast import router as podcast_router
from handlers.books import router as books_router

from handlers import (
    start,
    ordinary,
    premium,
    payment,
    admin
)


# =========================================================
# RENDER / WEBHOOK SETTINGS
# =========================================================

PORT = int(os.getenv("PORT", "8080"))

WEBHOOK_PATH = "/webhook"

# Render avtomatik beradi:
# RENDER_EXTERNAL_URL=https://your-bot.onrender.com
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST") or os.getenv(
    "RENDER_EXTERNAL_URL",
    ""
).rstrip("/")

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


# =========================================================
# BOT
# =========================================================

bot = Bot(
    token= os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


# =========================================================
# DISPATCHER
# =========================================================

dp = Dispatcher()


# =========================================================
# ROUTERS
# =========================================================

dp.include_router(start.router)

# Kitoblar — AVVAL
dp.include_router(books_router)

# AI Teacher
dp.include_router(ai_teacher_router)

# Asosiy routerlar
dp.include_router(ordinary.router)
dp.include_router(premium.router)
dp.include_router(payment.router)
dp.include_router(admin.router)

# Darslar
dp.include_router(letters_router)
dp.include_router(daily_grammar_router)
dp.include_router(admin_daily_grammar_router)
dp.include_router(grammar_router)

# Podcast
dp.include_router(podcast_router)


# =========================================================
# STARTUP
# =========================================================

async def on_startup():
    print("🤖 Korean School Bot ishga tushmoqda...")

    # Database
    init_db()
    print("✅ Database tayyor")

    # Token tekshirish
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN topilmadi. Environment Variables ni tekshiring!"
        )

    # Webhook URL tekshirish
    if not WEBHOOK_HOST:
        raise ValueError(
            "WEBHOOK_HOST yoki RENDER_EXTERNAL_URL topilmadi!"
        )

    print(f"🌐 Webhook URL: {WEBHOOK_URL}")

    # Eski webhookni tozalab, yangisini o'rnatamiz
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types()
    )

    print("✅ Webhook o'rnatildi!")
    print(f"🚀 Server PORT: {PORT}")


# =========================================================
# SHUTDOWN
# =========================================================

async def on_shutdown():
    print("🛑 Bot to'xtatilmoqda...")

    await bot.delete_webhook()

    await bot.session.close()

    print("✅ Bot to'xtadi")


# =========================================================
# WEB APPLICATION
# =========================================================

def create_app():

    app = web.Application()

    # Startup
    app.on_startup.append(
        lambda app: on_startup()
    )

    # Shutdown
    app.on_shutdown.append(
        lambda app: on_shutdown()
    )

    # Telegram webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )

    webhook_handler.register(
        app,
        path=WEBHOOK_PATH
    )

    # Aiogram application setup
    setup_application(
        app,
        dp,
        bot=bot
    )

    return app


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("🌐 Webhook server ishga tushmoqda...")

    app = create_app()

    web.run_app(
        app,
        host="0.0.0.0",
        port=PORT
    )
