from urllib.parse import quote

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID

from database import (
    add_user,
    add_referral,
    get_referral_count,
    get_referred_users,
    create_referral_premium_request,
    get_referral_premium_request,
    approve_referral_premium_request,
    reject_referral_premium_request,
    activate_premium,
    is_premium,
)

from keyboards.reply import (
    mode_menu,
    referral_menu,
)

from keyboards.inline import (
    referral_link_keyboard,
    referral_admin_keyboard,
)


router = Router()


# ============================================================
# SOZLAMALAR
# ============================================================

REFERRAL_REQUIRED = 5


# ============================================================
# REFERRAL LINK ORQALI KIRISH
# ============================================================

@router.message(CommandStart(deep_link=True))
async def referral_start(
    message: Message,
    command: CommandObject
):
    user = message.from_user

    # Foydalanuvchini bazaga qo'shamiz
    add_user(
        user_id=user.id,
        first_name=user.first_name or "",
        username=user.username,
    )

    args = command.args

    if not args:
        return

    if not args.startswith("ref_"):
        return

    try:
        referrer_id = int(
            args.replace("ref_", "", 1)
        )
    except ValueError:
        return

    # O'z linki orqali o'zini taklif qilish
    if referrer_id == user.id:
        return

    # Referralni saqlash
    added = add_referral(
        referrer_id=referrer_id,
        referred_id=user.id,
    )

    if not added:
        return

    # Referral egasining yangi soni
    count = get_referral_count(referrer_id)

    # Agar 5 taga yetgan bo'lsa
    if count == REFERRAL_REQUIRED:
        try:
            await message.bot.send_message(
                referrer_id,
                (
                    "🎉 <b>TABRIKLAYMIZ!</b>\n\n"
                    "Siz orqali botga "
                    "<b>5 ta yangi foydalanuvchi</b> kirdi! 👥\n\n"
                    "👑 Endi siz <b>UMRBOY PREMIUM</b> "
                    "uchun ariza berishingiz mumkin.\n\n"
                    "🎁 <b>Do‘stlarni taklif qilish</b> "
                    "bo‘limiga kirib ariza yuboring."
                )
            )
        except Exception:
            pass


# ============================================================
# DO'STLARNI TAKLIF QILISH
# ============================================================

@router.message(
    F.text == "🎁 Do‘stlarni taklif qilish"
)
async def referral_menu_handler(
    message: Message
):
    await message.answer(
        (
            "🎁 <b>DO‘STLARNI TAKLIF QILISH</b>\n\n"
            "Do‘stlaringizni taklif qiling va "
            "<b>5 ta yangi foydalanuvchi</b> "
            "olib kelganingizda UMRBOY PREMIUM oling! 👑"
        ),
        reply_markup=referral_menu()
    )


# ============================================================
# MEN QO'SHGAN ODAMLAR
# ============================================================

@router.message(
    F.text == "👥 Men qo‘shgan odamlar"
)
async def my_referrals(
    message: Message
):
    user_id = message.from_user.id

    count = get_referral_count(user_id)
    users = get_referred_users(user_id)

    remaining = max(
        REFERRAL_REQUIRED - count,
        0
    )

    if count >= REFERRAL_REQUIRED:
        status_text = (
            "🎉 <b>Premium olish sharti bajarildi!</b>"
        )
    else:
        status_text = (
            f"🎯 Premium uchun: "
            f"<b>{REFERRAL_REQUIRED}</b> ta\n\n"
            f"Yana <b>{remaining}</b> ta odam kerak."
        )

    text = (
        "👥 <b>MEN QO‘SHGAN ODAMLAR</b>\n\n"
        f"Siz orqali botga kirganlar: "
        f"<b>{count} ta</b>\n\n"
        f"{status_text}\n\n"
        "👥 <b>SIZ TAKLIF QILGAN ODAMLAR:</b>\n"
    )

    if not users:
        text += "\nHozircha hech kim yo‘q."

    else:
        for index, row in enumerate(users, start=1):

            first_name = (
                row["first_name"]
                or "Noma'lum"
            )

            username = row["username"]

            if username:
                user_text = (
                    f"{first_name} — @{username}"
                )
            else:
                user_text = (
                    f"{first_name} — username yo‘q"
                )

            text += (
                f"\n{index}. {user_text}"
            )

    await message.answer(text)


# ============================================================
# REFERAL LINKIM
# ============================================================

@router.message(
    F.text == "🔗 Referal linkim"
)
async def my_referral_link(
    message: Message
):
    user_id = message.from_user.id

    bot_info = await message.bot.get_me()

    bot_username = bot_info.username

    referral_link = (
        f"https://t.me/{bot_username}"
        f"?start=ref_{user_id}"
    )

    count = get_referral_count(user_id)

    text = (
        "🔗 <b>SIZNING REFERAL LINKINGIZ</b>\n\n"
        "Do‘stlaringizni quyidagi link orqali "
        "botga taklif qiling:\n\n"
        f"<code>{referral_link}</code>\n\n"
        f"👥 Siz qo‘shgan odamlar: "
        f"<b>{count}/{REFERRAL_REQUIRED}</b>"
    )

    await message.answer(
        text,
        reply_markup=referral_link_keyboard(
            referral_link
        )
    )


# ============================================================
# PREMIUMGA ARIZA
# ============================================================

@router.message(
    F.text == "👑 Premiumga ariza berish"
)
async def premium_request(
    message: Message
):
    user_id = message.from_user.id

    count = get_referral_count(user_id)

    # 5 ta bo'lmasa
    if count < REFERRAL_REQUIRED:

        remaining = (
            REFERRAL_REQUIRED - count
        )

        await message.answer(
            (
                "⏳ <b>Hali shart bajarilmagan.</b>\n\n"
                f"👥 Siz orqali kirganlar: "
                f"<b>{count} ta</b>\n"
                f"🎯 Premium uchun: "
                f"<b>{REFERRAL_REQUIRED} ta</b>\n\n"
                f"Yana <b>{remaining}</b> ta "
                "yangi odam taklif qilishingiz kerak."
            )
        )

        return

    # Allaqachon premium bo'lsa
    if is_premium(user_id):

        await message.answer(
            "👑 Sizda allaqachon UMRBOY PREMIUM mavjud!"
        )

        return

    # Ariza yaratish
    request_id = create_referral_premium_request(
        user_id
    )

    if request_id is None:

        await message.answer(
            "⏳ Sizning Premium arizangiz "
            "allaqachon admin ko‘rib chiqishida."
        )

        return

    # User ma'lumotlari
    user = message.from_user

    username_text = (
        f"@{user.username}"
        if user.username
        else "Username yo‘q"
    )

    # Admin xabari
    admin_text = (
        "🔔 <b>YANGI REFERRAL PREMIUM ARIZASI</b>\n\n"
        f"👤 <b>Ism:</b> "
        f"{user.first_name or 'Nomaʼlum'}\n"
        f"🔗 <b>Username:</b> "
        f"{username_text}\n"
        f"🆔 <b>Telegram ID:</b> "
        f"<code>{user.id}</code>\n\n"
        f"👥 <b>Taklif qilganlar:</b> "
        f"{count} ta\n\n"
        "🎁 Foydalanuvchi 5 ta yangi "
        "foydalanuvchini referral orqali "
        "olib keldi.\n\n"
        "👇 Qaror qiling:"
    )

    await message.bot.send_message(
        ADMIN_ID,
        admin_text,
        reply_markup=referral_admin_keyboard(
            request_id
        )
    )

    await message.answer(
        (
            "✅ <b>Arizangiz yuborildi!</b>\n\n"
            "Admin arizangizni ko‘rib chiqadi.\n"
            "Natija sizga bot orqali yuboriladi. 👑"
        )
    )


# ============================================================
# ADMIN — PREMIUM BERISH
# ============================================================

@router.callback_query(
    F.data.startswith("ref_premium_approve:")
)
async def approve_referral_premium(
    callback: CallbackQuery
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q!",
            show_alert=True
        )
        return

    request_id = int(
        callback.data.split(":")[1]
    )

    request = get_referral_premium_request(
        request_id
    )

    if not request:
        await callback.answer(
            "❌ Ariza topilmadi.",
            show_alert=True
        )
        return

    user_id = request["user_id"]

    # Premium beramiz
    activate_premium(user_id)

    # Arizani approved qilamiz
    approve_referral_premium_request(
        request_id=request_id,
        admin_id=callback.from_user.id
    )

    await callback.message.edit_text(
        callback.message.text
        + "\n\n"
        "✅ <b>PREMIUM BERILDI</b>"
    )

    await callback.bot.send_message(
        user_id,
        (
            "🎉 <b>TABRIKLAYMIZ!</b>\n\n"
            "Sizning referral Premium arizangiz "
            "admin tomonidan tasdiqlandi.\n\n"
            "👑 <b>UMRBOY PREMIUM</b> "
            "faollashtirildi!\n\n"
            "Endi Premium imkoniyatlaridan "
            "foydalanishingiz mumkin."
        )
    )

    await callback.answer(
        "✅ Premium berildi!"
    )


# ============================================================
# ADMIN — RAD ETISH
# ============================================================

@router.callback_query(
    F.data.startswith("ref_premium_reject:")
)
async def reject_referral_premium(
    callback: CallbackQuery
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Sizda ruxsat yo‘q!",
            show_alert=True
        )
        return

    request_id = int(
        callback.data.split(":")[1]
    )

    request = get_referral_premium_request(
        request_id
    )

    if not request:
        await callback.answer(
            "❌ Ariza topilmadi.",
            show_alert=True
        )
        return

    user_id = request["user_id"]

    reject_referral_premium_request(
        request_id=request_id,
        admin_id=callback.from_user.id
    )

    await callback.message.edit_text(
        callback.message.text
        + "\n\n"
        "❌ <b>ARIZA RAD ETILDI</b>"
    )

    await callback.bot.send_message(
        user_id,
        (
            "❌ <b>Premium arizangiz rad etildi.</b>\n\n"
            "Agar bu xatolik deb hisoblasangiz, "
            "admin bilan bog‘lanishingiz mumkin."
        )
    )

    await callback.answer(
        "❌ Ariza rad etildi."
    )
