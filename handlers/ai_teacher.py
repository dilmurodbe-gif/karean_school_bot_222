from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import (
    is_premium,
    get_ai_teacher_daily_count,
    create_ai_teacher_question,
    get_ai_teacher_question_by_admin_message,
    answer_ai_teacher_question
)

from config import ADMIN_ID


router = Router()


# ============================================================
# SETTINGS
# ============================================================

DAILY_LIMIT = 2


# ============================================================
# FSM STATES
# ============================================================

class AITeacherStates(StatesGroup):
    waiting_for_question = State()


# ============================================================
# AI TEACHER BUTTON
# ============================================================

@router.message(F.text == "🤖 AI Teacher")
async def open_ai_teacher(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    # Premium tekshirish
    if not is_premium(user_id):
        await message.answer(
            "🔒 <b>AI Teacher faqat Premium foydalanuvchilar uchun.</b>\n\n"
            "⭐ Premiumga o'ting va o'qituvchidan savol so'rang."
        )
        return

    # Bugungi foydalanish
    used = get_ai_teacher_daily_count(user_id)
    remaining = DAILY_LIMIT - used

    # Limit tugagan
    if remaining <= 0:
        await message.answer(
            "⚠️ <b>Bugungi AI Teacher limitingiz tugadi.</b>\n\n"
            "📊 Bugun: <b>2/2</b>\n"
            "📅 Ertaga yana 2 ta savol berishingiz mumkin."
        )
        return

    # Savol kutish holatiga o'tkazamiz
    await state.set_state(
        AITeacherStates.waiting_for_question
    )

    await message.answer(
        "🤖 <b>AI Teacher</b>\n\n"
        "🇰🇷 Koreys tili bo'yicha savolingizni yozing.\n\n"
        f"📊 Bugungi limit: <b>{remaining}/2</b>\n\n"
        "💡 Masalan:\n"
        "• 은/는 va 이/가 farqi nima?\n"
        "• Shu gapni tekshirib bering\n"
        "• Bu grammatikani tushuntiring\n"
        "• TOPIK uchun qanday ishlatiladi?\n\n"
        "❌ Bekor qilish uchun /cancel yozing."
    )


# ============================================================
# CANCEL
# ============================================================

@router.message(
    AITeacherStates.waiting_for_question,
    F.text == "/cancel"
)
async def cancel_ai_teacher(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await message.answer(
        "❌ <b>AI Teacher bekor qilindi.</b>\n\n"
        "Qayta savol bermoqchi bo'lsangiz "
        "🤖 AI Teacher tugmasini bosing."
    )


# ============================================================
# USER QUESTION
# ============================================================

@router.message(
    AITeacherStates.waiting_for_question,
    F.text
)
async def user_ai_teacher_question(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    # Premium tekshirish
    if not is_premium(user_id):
        await state.clear()

        await message.answer(
            "🔒 <b>AI Teacher faqat Premium foydalanuvchilar uchun.</b>"
        )
        return

    # Limitni qayta tekshirish
    used = get_ai_teacher_daily_count(user_id)

    if used >= DAILY_LIMIT:
        await state.clear()

        await message.answer(
            "⚠️ <b>Bugungi AI Teacher limitingiz tugadi.</b>\n\n"
            "📊 Bugun: <b>2/2</b>\n"
            "📅 Ertaga yana 2 ta savol berishingiz mumkin."
        )
        return

    # Savol
    question = message.text.strip()

    if not question:
        await message.answer(
            "❌ Iltimos, savolingizni matn ko'rinishida yuboring."
        )
        return

    username = (
        message.from_user.username
        or "username yo'q"
    )

    first_name = (
        message.from_user.first_name
        or "Noma'lum"
    )

    # Savol raqami
    question_number = used + 1

    # ========================================================
    # ADMIN'GA YUBORISH
    # ========================================================

    try:

        admin_message = await message.bot.send_message(
            ADMIN_ID,

            "🤖 <b>AI TEACHER — YANGI SAVOL</b>\n\n"

            f"🆔 <b>User ID:</b> "
            f"<code>{user_id}</code>\n"

            f"👤 <b>Ism:</b> "
            f"{first_name}\n"

            f"🔗 <b>Username:</b> "
            f"@{username}\n\n"

            f"📊 <b>Bugungi savol:</b> "
            f"{question_number}/{DAILY_LIMIT}\n\n"

            f"❓ <b>Savol:</b>\n"
            f"{question}\n\n"

            "💬 Javob berish uchun "
            "<b>shu xabarga Reply</b> qiling."
        )

    except Exception as e:

        print(
            f"[AI TEACHER] Admin'ga xabar yuborishda xato: {e}"
        )

        await message.answer(
            "❌ <b>Hozircha savolni o'qituvchiga yuborib bo'lmadi.</b>\n\n"
            "Iltimos, birozdan keyin qayta urinib ko'ring."
        )

        return

    # ========================================================
    # DATABASE
    # ========================================================

    try:

        question_id = create_ai_teacher_question(
            user_id=user_id,
            username=username,
            first_name=first_name,
            question=question,
            admin_message_id=admin_message.message_id
        )

        print(
            f"[AI TEACHER] Yangi savol saqlandi: {question_id}"
        )

    except Exception as e:

        print(
            f"[AI TEACHER] Database xatosi: {e}"
        )

        await message.answer(
            "❌ Savolni saqlashda xatolik yuz berdi."
        )

        return

    # Savol yuborilgandan keyin state tozalaymiz
    await state.clear()

    # Qolgan limit
    remaining = DAILY_LIMIT - question_number

    # ========================================================
    # USERGA TASDIQ
    # ========================================================

    await message.answer(
        "✅ <b>Savolingiz o'qituvchiga yuborildi!</b>\n\n"

        "👨‍🏫 O'qituvchi javob berganidan keyin "
        "javob sizga shu yerga keladi.\n\n"

        f"📊 Bugungi foydalanish: "
        f"<b>{question_number}/{DAILY_LIMIT}</b>\n"

        f"🔢 Qolgan: "
        f"<b>{remaining}</b>"
    )


# ============================================================
# USER SENDS NON-TEXT WHILE WAITING
# ============================================================

@router.message(
    AITeacherStates.waiting_for_question
)
async def ai_teacher_non_text(
    message: Message
):

    await message.answer(
        "❌ <b>Iltimos, savolingizni matn ko'rinishida yozing.</b>\n\n"
        "Masalan:\n"
        "🇰🇷 은/는 va 이/가 farqi nima?"
    )


# ============================================================
# ADMIN REPLY
# ============================================================

@router.message(
    F.reply_to_message,
    lambda message: message.from_user.id == ADMIN_ID
)
async def admin_reply_to_teacher(
    message: Message
):

    replied_message = message.reply_to_message

    if not replied_message:
        return

    # Admin reply qilgan xabar AI Teacher savolimi?
    question = get_ai_teacher_question_by_admin_message(
        replied_message.message_id
    )

    if not question:
        return

    # Oldin javob berilganmi?
    if question["status"] == "answered":

        await message.answer(
            "⚠️ <b>Bu savolga allaqachon javob berilgan.</b>"
        )

        return

    # Faqat text javob
    if not message.text:

        await message.answer(
            "❌ <b>Javob matn ko'rinishida bo'lishi kerak.</b>"
        )

        return

    answer = message.text.strip()

    if not answer:
        return

    user_id = question["user_id"]

    # ========================================================
    # USERGA JAVOB
    # ========================================================

    try:

        await message.bot.send_message(
            user_id,

            "👨‍🏫 <b>AI Teacher javobi:</b>\n\n"
            f"{answer}"
        )

    except Exception as e:

        print(
            f"[AI TEACHER] Userga javob yuborishda xato: {e}"
        )

        await message.answer(
            "❌ <b>Foydalanuvchiga javob yuborib bo'lmadi.</b>\n\n"
            f"<code>{e}</code>"
        )

        return

    # ========================================================
    # DATABASE UPDATE
    # ========================================================

    try:

        answer_ai_teacher_question(
            question_id=question["id"],
            answer=answer
        )

    except Exception as e:

        print(
            f"[AI TEACHER] Javobni databasega saqlashda xato: {e}"
        )

        await message.answer(
            "⚠️ Javob foydalanuvchiga yuborildi, "
            "lekin databasega saqlashda xato bo'ldi."
        )

        return

    # ========================================================
    # ADMIN CONFIRMATION
    # ========================================================

    await message.answer(
        "✅ <b>Javob foydalanuvchiga yuborildi.</b>"
    )
