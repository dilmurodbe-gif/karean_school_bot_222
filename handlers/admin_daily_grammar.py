from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime, timedelta

from config import ADMIN_IDS
from database import (
    create_daily_grammar,
    delete_daily_grammar,
    get_daily_grammar
)


router = Router()


# Admin vaqtinchalik holatlari
daily_grammar_state = {}
daily_grammar_temp = {}


# ==========================================
# BUGUNGI GRAMMATIKANI QO'SHISHNI BOSHLASH
# ==========================================

@router.message(F.text == "➕ Bugungi grammatikani qo‘shish")
async def daily_grammar_add_start(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    daily_grammar_state[message.from_user.id] = "wait_photo"
    daily_grammar_temp[message.from_user.id] = {}

    await message.answer(
        "📌 BUGUNGI GRAMMATIKANI QO‘SHISH\n\n"
        "1️⃣ Avval rasm yuboring 🖼\n"
        "2️⃣ Keyin grammatika matnini yuborasiz ✍️\n\n"
        "💡 Rasm bilan birga caption yozsangiz, "
        "grammatika avtomatik saqlanadi.\n\n"
        "⏰ Grammatika 24 soat davomida ko‘rinadi."
    )


# ==========================================
# RASMNI OLISH
# ==========================================

@router.message(
    lambda message: daily_grammar_state.get(
        message.from_user.id
    ) == "wait_photo"
)
async def daily_grammar_get_photo(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    if not message.photo:
        await message.answer(
            "❌ Iltimos, faqat rasm yuboring."
        )
        return

    file_id = message.photo[-1].file_id

    daily_grammar_temp[message.from_user.id] = {
        "photo": file_id
    }

    # Caption bo'lsa darrov saqlaymiz
    caption = (message.caption or "").strip()

    if caption:
        expires_at = (
            datetime.now() + timedelta(hours=24)
        ).isoformat()

        create_daily_grammar(
            photo_file_id=file_id,
            text=caption,
            expires_at=expires_at
        )

        daily_grammar_state.pop(message.from_user.id, None)
        daily_grammar_temp.pop(message.from_user.id, None)

        await message.answer(
            "✅ Bugungi grammatika muvaffaqiyatli saqlandi!\n\n"
            "⏰ 24 soat davomida ko‘rinadi."
        )

        await message.answer_photo(
            photo=file_id,
            caption=(
                "📅 Bugungi grammatika (PREVIEW)\n\n"
                f"{caption}"
            )
        )

        return

    # Caption bo'lmasa matnni kutamiz
    daily_grammar_state[message.from_user.id] = "wait_text"

    await message.answer(
        "✍️ Endi rasm tagida chiqadigan "
        "matnni yuboring:"
    )


# ==========================================
# MATNNI OLISH
# ==========================================

@router.message(
    lambda message: daily_grammar_state.get(
        message.from_user.id
    ) == "wait_text"
)
async def daily_grammar_get_text(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    text = (message.text or "").strip()

    if not text:
        await message.answer(
            "❌ Matn bo‘sh bo‘lmasligi kerak.\n\n"
            "Qaytadan yuboring."
        )
        return

    photo_id = daily_grammar_temp.get(
        message.from_user.id,
        {}
    ).get("photo")

    if not photo_id:
        daily_grammar_state.pop(message.from_user.id, None)
        daily_grammar_temp.pop(message.from_user.id, None)

        await message.answer(
            "❌ Rasm topilmadi.\n\n"
            "Qaytadan boshlang:\n"
            "➕ Bugungi grammatikani qo‘shish"
        )
        return

    expires_at = (
        datetime.now() + timedelta(hours=24)
    ).isoformat()

    create_daily_grammar(
        photo_file_id=photo_id,
        text=text,
        expires_at=expires_at
    )

    daily_grammar_state.pop(message.from_user.id, None)
    daily_grammar_temp.pop(message.from_user.id, None)

    await message.answer(
        "✅ Bugungi grammatika muvaffaqiyatli saqlandi!\n\n"
        "⏰ 24 soat davomida ko‘rinadi."
    )

    await message.answer_photo(
        photo=photo_id,
        caption=(
            "📅 Bugungi grammatika (PREVIEW)\n\n"
            f"{text}"
        )
    )


# ==========================================
# BUGUNGI GRAMMATIKANI O'CHIRISH
# ==========================================

@router.message(F.text == "❌ Bugungi grammatikani o‘chirish")
async def delete_daily_grammar_handler(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        return

    row = get_daily_grammar()

    if not row:
        await message.answer(
            "📭 Hozircha o‘chiriladigan "
            "bugungi grammatika yo‘q."
        )
        return

    delete_daily_grammar()

    await message.answer(
        "✅ Bugungi grammatika muvaffaqiyatli o‘chirildi."
    )
