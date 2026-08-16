from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import REQUIRED_CHANNEL
from database import add_user
from keyboards.reply import mode_menu
from keyboards.inline import subscribe_keyboard


router = Router()


def get_channel_url():
    if REQUIRED_CHANNEL.startswith("@"):
        return f"https://t.me/{REQUIRED_CHANNEL[1:]}"
    return REQUIRED_CHANNEL


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=REQUIRED_CHANNEL,
            user_id=user_id
        )

        return member.status in [
            "creator",
            "administrator",
            "member"
        ]

    except Exception:
        return False


async def show_mode_selection(message: Message):
    await message.answer(
        "👋 Assalomu alaykum va xush kelibsiz!\n\n"
        "🇰🇷 <b>Korean School</b> — koreys tilini oson va qulay "
        "o‘rganishingiz uchun yaratilgan bot! ✨\n\n"
        "📚 O‘zingizga kerakli bo‘limni tanlang va o‘rganishni boshlang 👇\n\n"
        "ℹ️ Bot haqida batafsil ma’lumot olish uchun <b>«Bot haqida»</b> "
        "tugmasini bosing.",
        reply_markup=mode_menu()
    )


@router.message(Command("start"))
async def start_command(message: Message, bot: Bot):
    user = message.from_user

    add_user(
        user_id=user.id,
        first_name=user.first_name,
        username=user.username
    )

    if not REQUIRED_CHANNEL:
        await show_mode_selection(message)
        return

    subscribed = await is_subscribed(bot, user.id)

    if subscribed:
        await show_mode_selection(message)
        return

    await message.answer(
        "📢 Botdan foydalanish uchun avval kanalimizga a'zo bo'ling.\n\n"
        "A'zo bo'lgach, pastdagi «✅ Tekshirish» tugmasini bosing.",
        reply_markup=subscribe_keyboard(get_channel_url())
    )


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery, bot: Bot):
    subscribed = await is_subscribed(
        bot,
        callback.from_user.id
    )

    if not subscribed:
        await callback.answer(
            "❌ Siz hali kanalga a'zo bo'lmagansiz!",
            show_alert=True
        )
        return

    await callback.answer("✅ Tekshirildi!")
    await callback.message.delete()
    await show_mode_selection(callback.message)
