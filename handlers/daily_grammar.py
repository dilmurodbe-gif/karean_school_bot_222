from aiogram import Router, F
from aiogram.types import Message

from datetime import datetime, timedelta

from database import (
    get_daily_grammar,
    expire_daily_grammar,
    increase_daily_grammar_views
)


router = Router()


@router.message(F.text == "📅 Bugungi grammatika")
async def show_daily_grammar(message: Message):

    row = get_daily_grammar()

    # Grammatika yo'q
    if not row:
        await message.answer(
            "📭 Buguncha grammatika joylanmagan."
        )
        return

    photo_id = row["photo_file_id"]
    text = row["text"]
    expires_at = row["expires_at"]

    # Muddatni tekshirish
    try:
        exp = datetime.fromisoformat(expires_at)
    except Exception:
        exp = datetime.now() - timedelta(seconds=1)

    # Muddati tugagan
    if datetime.now() >= exp:

        expire_daily_grammar()

        await message.answer(
            "⏳ Bugungi grammatika muddati tugagan.\n"
            "Yangi grammatika kutilmoqda ✅"
        )
        return

    # Ko'rishlar sonini +1 qilish
    increase_daily_grammar_views()

    caption = (
        "📅 <b>BUGUNGI GRAMMATIKA</b>\n\n"
        f"{text or ''}"
    )

    # Rasm bo'lsa
    if photo_id:
        await message.answer_photo(
            photo=photo_id,
            caption=caption
        )

    # Rasm bo'lmasa faqat matn
    else:
        await message.answer(caption)
