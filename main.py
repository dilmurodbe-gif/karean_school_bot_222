import asyncio
import os

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

# ============================================================
# HANDLERS
# ============================================================

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


# ============================================================
# WEBHOOK SETTINGS
# ============================================================

WEBHOOK_PATH = "/webhook"
HOST = "0.0.0.0"


async def on_startup(bot: Bot, webhook_url: str):
    """
    Bot ishga tushganda Telegram webhook o'rnatiladi.
    """

    webhook_info = await bot.get_webhook_info()

    if webhook_info.url != webhook_url:
        await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True,
        )

    print("🤖 Korean School Bot webhook rejimida ishga tushdi!")
    print(f"🌐 Webhook URL: {webhook_url}")


async def main():
    # ========================================================
    # ENVIRONMENT VARIABLES
    # ========================================================

    webhook_base_url = os.getenv("WEBHOOK_URL", "").strip()

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN topilmadi. "
            "Render Environment Variables yoki .env faylini tekshiring!"
        )

    if not webhook_base_url:
        raise ValueError(
            "WEBHOOK_URL topilmadi. "
            "Render Environment Variables ga qo'shing!"
        )

    # Masalan:
    # WEBHOOK_URL=https://your-service.onrender.com
    webhook_full_url = (
        webhook_base_url.rstrip("/") + WEBHOOK_PATH
    )

    # ========================================================
    # PORT
    # ========================================================

    port = int(os.getenv("PORT", "10000"))

    # ========================================================
    # DATABASE
    # ========================================================

    init_db()
    print("🗄️ Database tayyor!")

    # ========================================================
    # BOT
    # ========================================================

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # ========================================================
    # DISPATCHER
    # ========================================================

    dp = Dispatcher()

    # ========================================================
    # ROUTERS
    # ========================================================

    # START
    dp.include_router(start.router)

    # KITOBLAR
    dp.include_router(books_router)

    # AI TEACHER
    dp.include_router(ai_teacher_router)

    # ASOSIY ROUTERLAR
    dp.include_router(ordinary.router)
    dp.include_router(premium.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)

    # DARSLAR
    dp.include_router(letters_router)
    dp.include_router(daily_grammar_router)
    dp.include_router(admin_daily_grammar_router)
    dp.include_router(grammar_router)

    # PODCAST
    dp.include_router(podcast_router)

    print("📦 Barcha routerlar yuklandi!")

    # ========================================================
    # AIOHTTP APPLICATION
    # ========================================================

    app = web.Application()

    # ========================================================
    # TELEGRAM WEBHOOK HANDLER
    # ========================================================

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )

    webhook_handler.register(
        app,
        path=WEBHOOK_PATH,
    )

    # Aiogram lifecycle
    setup_application(
        app,
        dp,
        bot=bot,
    )

    # ========================================================
    # START SERVER
    # ========================================================

    runner = web.AppRunner(app)

    try:
        await runner.setup()

        site = web.TCPSite(
            runner,
            host=HOST,
            port=port,
        )

        await site.start()

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🚀 Server muvaffaqiyatli ishga tushdi!")
        print(f"🌐 Server: {HOST}:{port}")
        print(f"🔗 Webhook: {webhook_full_url}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Server ishga tushgandan KEYIN webhook o'rnatamiz
        await on_startup(
            bot=bot,
            webhook_url=webhook_full_url,
        )

        # Server doim ishlab turadi
        await asyncio.Event().wait()

    finally:
        print("🛑 Server to'xtatilmoqda...")

        await runner.cleanup()

        await bot.session.close()

        print("👋 Bot to'xtatildi!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot qo'lda to'xtatildi.")
