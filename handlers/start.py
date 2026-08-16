from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatMemberStatus

from config import REQUIRED_CHANNEL
from database import add_user
from keyboards.reply import mode_menu
from keyboards.inline import subscribe_keyboard


router = Router()


# ============================================================
# CHANNEL URL
# ============================================================

def get_channel_url():
    """
    Kanal username'dan URL yaratadi.
    Masalan:
    @korean_school -> https://t.me/korean_school
    """

    if REQUIRED_CHANNEL and REQUIRED_CHANNEL.startswith("@"):
        return f"https://t.me/{REQUIRED_CHANNEL[1:]}"

    return REQUIRED_CHANNEL


# ============================================================
# CHECK SUBSCRIPTION
# ============================================================

async def is_subscribed(bot: Bot, user_id: int) -> bool:
    """
    Foydalanuvchi majburiy kanalga a'zo ekanligini tekshiradi.
    """

    # Kanal sozlanmagan bo'lsa, obunani tekshirmaymiz
    if not REQUIRED_CHANNEL:
        return True

    try:
        member = await bot.get_chat_member(
            chat_id=REQUIRED_CHANNEL,
            user_id=user_id
        )

        print(
            f"👤 User: {user_id} | "
            f"Channel status: {member.status}"
        )

        return member.status in [
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]

    except Exception as e:
        print(
            f"❌ Kanal obunasini tekshirishda xato: {e}"
        )
        return False


# ============================================================
# SHOW MAIN MENU
# ============================================================

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


# ============================================================
# START COMMAND
# ============================================================

@router.message(CommandStart())
async def start_command(message: Message, bot: Bot):
    print(f"🔥 /START KELDI: {message.from_user.id}")

    user = message.from_user

    # --------------------------------------------------------
    # SAVE USER
    # --------------------------------------------------------

    try:
        add_user(
            user_id=user.id,
            first_name=user.first_name,
            username=user.username
        )

        print(f"✅ User saqlandi: {user.id}")

    except Exception as e:
        print(f"❌ User saqlashda xato: {e}")

    # --------------------------------------------------------
    # CHANNEL CHECK
    # --------------------------------------------------------

    if not REQUIRED_CHANNEL:
        print("ℹ️ REQUIRED_CHANNEL sozlanmagan.")
        await show_mode_selection(message)
        return

    print(f"📢 Kanal tekshirilmoqda: {REQUIRED_CHANNEL}")

    subscribed = await is_subscribed(
        bot,
        user.id
    )

    # --------------------------------------------------------
    # USER SUBSCRIBED
    # --------------------------------------------------------

    if subscribed:
        print("✅ User kanalga a'zo.")
        await show_mode_selection(message)
        return

    # --------------------------------------------------------
    # USER NOT SUBSCRIBED
    # --------------------------------------------------------

    print("❌ User kanalga a'zo emas.")

    await message.answer(
        "📢 Botdan foydalanish uchun avval kanalimizga a'zo bo'ling.\n\n"
        "A'zo bo'lgach, pastdagi «✅ Tekshirish» tugmasini bosing.",
        reply_markup=subscribe_keyboard(get_channel_url())
    )


# ============================================================
# CHECK SUBSCRIPTION BUTTON
# ============================================================

@router.callback_query(F.data == "check_subscription")
async def check_subscription(
    callback: CallbackQuery,
    bot: Bot
):
    print(
        f"🔍 Obuna tekshirilmoqda: "
        f"{callback.from_user.id}"
    )

    subscribed = await is_subscribed(
        bot,
        callback.from_user.id
    )

    # --------------------------------------------------------
    # NOT SUBSCRIBED
    # --------------------------------------------------------

    if not subscribed:
        await callback.answer(
            "❌ Siz hali kanalga a'zo bo'lmagansiz!",
            show_alert=True
        )
        return

    # --------------------------------------------------------
    # SUBSCRIBED
    # --------------------------------------------------------

    await callback.answer(
        "✅ Tekshirildi!"
    )

    try:
        await callback.message.delete()
    except Exception as e:
        print(f"⚠️ Xabarni o'chirishda xato: {e}")

    await show_mode_selection(
        callback.message
    )
