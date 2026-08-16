import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN
from database import init_db

from handlers.ai_teacher import router as ai_teacher_router
from handlers.letters import router as letters_router
from handlers.daily_grammar import router as daily_grammar_router
from handlers.admin_daily_grammar import router as admin_daily_grammar_router
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


# ============================================================
# WEBHOOK SETTINGS
# ============================================================

WEBHOOK_PATH = "/webhook"

# Render o'zining PORT environment variable'ini beradi
HOST = "0.0.0.0"


async def main():

    # ========================================================
    # DATABASE
    # ========================================================

    init_db()

    # ========================================================
    # TOKEN
    # ========================================================

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN topilmadi. .env yoki Render Environment Variables ni tekshiring!"
        )

    # ========================================================
    # RENDER URL
    # ========================================================

    # Render'da WEBHOOK_URL environment variable bo'lishi kerak
    import os

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    if not WEBHOOK_URL:
        raise ValueError(
            "WEBHOOK_URL topilmadi. Render Environment Variables ga qo'shing!"
        )

    # ========================================================
    # BOT
    # ========================================================

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # ========================================================
    # DISPATCHER
    # ========================================================

    dp = Dispatcher()

    # ========================================================
    # ROUTERS
    # ========================================================

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

    print("🤖 Korean School Bot webhook rejimida ishga tushdi!")

    # ========================================================
    # WEB APP
    # ========================================================

    app = web.Application()

    # Telegram webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_handler.register(
        app,
        path=WEBHOOK_PATH
    )

    # Aiogram application lifecycle
    setup_application(
        app,
        dp,
        bot=bot
    )

    # ========================================================
    # WEBHOOK URL
    # ========================================================

    webhook_full_url = WEBHOOK_URL.rstrip("/") + WEBHOOK_PATH

    await bot.set_webhook(
        url=webhook_full_url,
        drop_pending_updates=True
    )

    print(f"🌐 Webhook: {webhook_full_url}")

    # ========================================================
    # PORT
    # ========================================================

    port = int(os.getenv("PORT", 10000))

    print(f"🚀 Server: {HOST}:{port}")

    # ========================================================
    # START SERVER
    # ========================================================

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        HOST,
        port
    )

    await site.start()

    print("✅ Server muvaffaqiyatli ishga tushdi!")

    # Server doim ishlab turishi kerak
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
