from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database import (
    is_premium,
    get_courses,
    get_course_by_code,
    get_sections,
    get_lessons
)

from keyboards.reply import premium_menu
from keyboards.inline import (
    premium_locked_keyboard,
    courses_keyboard,
    sections_keyboard,
    lessons_keyboard
)


router = Router()


@router.message(F.text == "💎 Premium")
async def premium_section(message: Message):
    user_id = message.from_user.id

    if not is_premium(user_id):
        await message.answer(
            "🔒 PREMIUM BO'LIM YOPIQ\n\n"
            "Siz hali Premiumga obuna bo'lmagansiz.\n\n"
            "Premiumga obuna bo'lsangiz barcha kurslar ochiladi:\n\n"
            "🌱 Boshlang'ich\n"
            "🥉 TOPIK 1\n"
            "🥇 TOPIK 2\n\n"
            "🎬 Barcha video darslardan foydalanishingiz mumkin.",
            reply_markup=premium_locked_keyboard()
        )
        return

    await message.answer(
        "💎 PREMIUM BO'LIMGA XUSH KELIBSIZ!\n\n"
        "Sizning Premiumingiz faol. 🎉\n"
        "Barcha kurslar siz uchun ochiq.",
        reply_markup=premium_menu()
    )


async def show_course(message_or_callback, code: str):
    course = get_course_by_code(code)

    if not course:
        return

    sections = get_sections(course["id"])

    text = (
        f"{course['title']}\n\n"
        f"{course['description'] or ''}\n\n"
    )

    if not sections:
        text += "⏳ Bu kursga hali bo'limlar qo'shilmagan."
        await message_or_callback.answer(text)
        return

    text += "📚 Bo'limni tanlang 👇"

    await message_or_callback.answer(
        text,
        reply_markup=sections_keyboard(sections)
    )


@router.message(F.text == "🌱 Boshlang'ich")
async def beginner_course(message: Message):
    if not is_premium(message.from_user.id):
        return

    await show_course(message, "beginner")


@router.message(F.text == "🥉 TOPIK 1")
async def topik1_course(message: Message):
    if not is_premium(message.from_user.id):
        return

    await show_course(message, "topik1")


@router.message(F.text == "🥇 TOPIK 2")
async def topik2_course(message: Message):
    if not is_premium(message.from_user.id):
        return

    await show_course(message, "topik2")


@router.callback_query(F.data.startswith("course:"))
async def open_course(callback: CallbackQuery):
    if not is_premium(callback.from_user.id):
        await callback.answer(
            "Premium faol emas!",
            show_alert=True
        )
        return

    code = callback.data.split(":", 1)[1]

    course = get_course_by_code(code)

    if not course:
        await callback.answer("Kurs topilmadi!", show_alert=True)
        return

    sections = get_sections(course["id"])

    if not sections:
        await callback.message.answer(
            "⏳ Bu kursga hali bo'limlar qo'shilmagan."
        )
        await callback.answer()
        return

    await callback.message.answer(
        f"{course['title']}\n\n📚 Bo'limni tanlang 👇",
        reply_markup=sections_keyboard(sections)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("section:"))
async def open_section(callback: CallbackQuery):
    if not is_premium(callback.from_user.id):
        await callback.answer(
            "Premium faol emas!",
            show_alert=True
        )
        return

    section_id = int(callback.data.split(":", 1)[1])

    lessons = get_lessons(section_id)

    if not lessons:
        await callback.message.answer(
            "⏳ Bu bo'limga hali video dars qo'shilmagan."
        )
        await callback.answer()
        return

    await callback.message.answer(
        "🎬 Video darsni tanlang 👇",
        reply_markup=lessons_keyboard(lessons)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("lesson:"))
async def open_lesson(callback: CallbackQuery):
    if not is_premium(callback.from_user.id):
        await callback.answer(
            "Premium faol emas!",
            show_alert=True
        )
        return

    import sqlite3
    from config import DATABASE_PATH

    lesson_id = int(callback.data.split(":", 1)[1])

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM video_lessons
        WHERE id=?
    """, (lesson_id,))

    lesson = cur.fetchone()
    conn.close()

    if not lesson:
        await callback.answer(
            "Dars topilmadi!",
            show_alert=True
        )
        return

    if not lesson["video_file_id"]:
        await callback.message.answer(
            f"🎬 {lesson['title']}\n\n"
            "⏳ Video hali qo'shilmagan."
        )
        await callback.answer()
        return

    await callback.message.answer_video(
        video=lesson["video_file_id"],
        caption=(
            f"🎬 {lesson['title']}\n\n"
            f"{lesson['description'] or ''}"
        )
    )

    await callback.answer()
