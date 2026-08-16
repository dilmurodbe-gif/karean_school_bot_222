import os
import asyncio

from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from config import BOT_TOKEN
from database import init_db

# =========================================================
# HANDLERS
# =========================================================

from handlers.ai_teacher import router as ai_teacher_router
from handlers.letters import router as letters_router
from handlers.daily_grammar import router as daily_grammar_router
from handlers.admin_daily_grammar import (
    router as admin_daily_grammar_router,
)
from handlers.grammar import router as grammar_router
from handlers.podcast import router as podcast_router
from handlers.books import router as books_router

from handlers import (
    start,
    ordinary,
    premium,
    payment,
    admin,
)


# =========================================================
# RENDER / WEBHOOK SETTINGS
# =========================================================

PORT = int(os.getenv("PORT", "8080"))

WEBHOOK_PATH = "/webhook"

# Render avtomatik beradi:
# https://karean-school-bot-222-1.onrender.com
WEBHOOK_HOST = (
    os.getenv("WEBHOOK_HOST")
    or os.getenv("RENDER_EXTERNAL_URL")
    or ""
).rstrip("/")

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


# =========================================================
# BOT
# =========================================================

if not BOT_TOKEN:
    raise ValueError(
        "❌ BOT_TOKEN topilmadi! "
        "Render Environment Variables ni tekshiring."
    )

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
)


# =========================================================
# DISPATCHER
# =========================================================

dp = Dispatcher()


# =========================================================
# ROUTERS
# =========================================================

dp.include_router(start.router)

# Kitoblar
dp.include_router(books_router)

# AI Teacher
dp.include_router(ai_teacher_router)

# Asosiy bo‘limlar
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
    print("========================================")
    print("🤖 Korean School Bot ishga tushmoqda...")
    print("========================================")

    # -----------------------------------------
    # DATABASE
    # -----------------------------------------

    try:
        init_db()
        print("✅ Database tayyor")
    except Exception as e:
        print(f"❌ Database xatosi: {e}")
        raise

    # -----------------------------------------
    # BOT TOKEN
    # -----------------------------------------

    if not BOT_TOKEN:
        raise ValueError(
            "❌ BOT_TOKEN topilmadi!"
        )

    print("✅ BOT_TOKEN topildi")

    # -----------------------------------------
    # WEBHOOK HOST
    # -----------------------------------------

    if not WEBHOOK_HOST:
        raise ValueError(
            "❌ WEBHOOK_HOST yoki RENDER_EXTERNAL_URL topilmadi!"
        )

    print(f"🌐 WEBHOOK_HOST: {WEBHOOK_HOST}")
    print(f"🔗 WEBHOOK_URL: {WEBHOOK_URL}")

    # -----------------------------------------
    # BOT INFO
    # -----------------------------------------

    try:
        bot_info = await bot.get_me()

        print(
            f"🤖 Bot: @{bot_info.username}"
        )

        print(
            f"🆔 Bot ID: {bot_info.id}"
        )

    except Exception as e:
        print(f"❌ Telegram bilan ulanish xatosi: {e}")
        raise

    # -----------------------------------------
    # OLD WEBHOOK
    # -----------------------------------------

    print("🧹 Eski webhook o‘chirilmoqda...")

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    print("✅ Eski webhook o‘chirildi")

    # -----------------------------------------
    # NEW WEBHOOK
    # -----------------------------------------

    print("📡 Yangi webhook o‘rnatilmoqda...")

    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
    )

    # -----------------------------------------
    # WEBHOOK INFO
    # -----------------------------------------

    webhook_info = await bot.get_webhook_info()

    print("========================================")
    print("✅ WEBHOOK MUVAFFAQIYATLI O‘RNATILDI")
    print("========================================")
    print(f"🌐 URL: {webhook_info.url}")
    print(f"📦 Pending updates: {webhook_info.pending_update_count}")
    print(f"❌ Last error: {webhook_info.last_error_message}")
    print(f"🕐 Last error date: {webhook_info.last_error_date}")
    print(f"🚀 PORT: {PORT}")
    print("========================================")
    print("🔥 Korean School Bot ONLINE!")
    print("========================================")


# =========================================================
# SHUTDOWN
# =========================================================

async def on_shutdown():
    print("========================================")
    print("🛑 Korean School Bot to‘xtatilmoqda...")
    print("========================================")

    try:
        await bot.delete_webhook()
        print("✅ Webhook o‘chirildi")
    except Exception as e:
        print(f"⚠️ Webhook o‘chirishda xato: {e}")

    try:
        await bot.session.close()
        print("✅ Telegram session yopildi")
    except Exception as e:
        print(f"⚠️ Session yopishda xato: {e}")

    print("🛑 Bot to‘xtadi")


# =========================================================
# AIOHTTP STARTUP / SHUTDOWN
# =========================================================

async def startup(app: web.Application):
    await on_startup()


async def shutdown(app: web.Application):
    await on_shutdown()


# =========================================================
# WEB APPLICATION
# =========================================================

def create_app():

    print("🌐 Web Application yaratilmoqda...")

    app = web.Application()

    # -----------------------------------------
    # STARTUP / SHUTDOWN
    # -----------------------------------------

    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)

    # -----------------------------------------
    # TELEGRAM WEBHOOK
    # -----------------------------------------

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_handler.register(
        app,
        path=WEBHOOK_PATH,
    )

    # -----------------------------------------
    # AIOGRAM APPLICATION
    # -----------------------------------------

    setup_application(
        app,
        dp,
        bot=bot,
    )

    # -----------------------------------------
    # HEALTH CHECK
    # -----------------------------------------

    async def health_check(request):
        return web.Response(
            text="Korean School Bot is ONLINE 🤖"
        )

    app.router.add_get(
        "/",
        health_check,
    )

    return app


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("========================================")
    print("🚀 KOREAN SCHOOL BOT")
    print("🚀 RENDER WEBHOOK SERVER")
    print("========================================")

    print(f"📡 PORT: {PORT}")
    print(f"🌐 WEBHOOK_HOST: {WEBHOOK_HOST}")
    print(f"🔗 WEBHOOK_URL: {WEBHOOK_URL}")

    app = create_app()

    web.run_app(
        app,
        host="0.0.0.0",
        port=PORT,
    )
