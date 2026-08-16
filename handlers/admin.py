import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID

from database import (
    get_payment,
    approve_payment,
    reject_payment,
    activate_premium,
    deactivate_premium,

    get_courses,
    get_sections,
    get_lessons,

    get_all_users,
    get_all_premium_users,
    get_users_count,
    get_premium_count,
    get_pending_payments_count,

    get_section,
    delete_section,

    get_lesson,
    delete_lesson,
    update_lesson_title,
    update_lesson_description,
    update_lesson_video,

    get_user_by_id
)

from keyboards.reply import admin_menu

from keyboards.inline import (
    admin_courses_keyboard,
    admin_sections_keyboard,
    admin_lessons_keyboard,
    admin_payment_keyboard,
    confirm_delete_section_keyboard,
    confirm_delete_lesson_keyboard
)

from states import AdminCourseState


router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ==========================================
# ADMIN PANEL
# ==========================================

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🛠 <b>ADMIN PANEL</b>\n\n"
        "Kerakli bo'limni tanlang 👇",
        reply_markup=admin_menu()
    )


# ==========================================
# TO'LOVLARNI TASDIQLASH
# ==========================================

@router.callback_query(F.data.startswith("payment_approve:"))
async def approve_payment_callback(
    callback: CallbackQuery,
    bot: Bot
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "❌ Siz admin emassiz!",
            show_alert=True
        )
        return

    payment_id = int(callback.data.split(":", 1)[1])

    payment = get_payment(payment_id)

    if not payment:
        await callback.answer(
            "❌ To'lov topilmadi!",
            show_alert=True
        )
        return

    if payment["status"] != "pending":
        await callback.answer(
            "⚠️ Bu to'lov allaqachon ko'rib chiqilgan.",
            show_alert=True
        )
        return

    approve_payment(
        payment_id,
        callback.from_user.id
    )

    activate_premium(payment["user_id"])

    try:
        await callback.message.edit_caption(
            caption=(
                callback.message.caption
                + "\n\n✅ <b>TO'LOV TASDIQLANDI</b>"
            ),
            reply_markup=None
        )
    except Exception:
        pass

    await bot.send_message(
        payment["user_id"],
        "🎉 <b>TABRIKLAYMIZ!</b>\n\n"
        "To'lovingiz tasdiqlandi va Premium muvaffaqiyatli "
        "faollashtirildi! 💎\n\n"
        "Endi barcha kurslarga kirishingiz mumkin:\n\n"
        "🌱 Boshlang'ich\n"
        "🥉 TOPIK 1\n"
        "🥇 TOPIK 2"
    )

    await callback.answer(
        "✅ Premium faollashtirildi!"
    )

def referral_admin_keyboard(request_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Premium berish",
                    callback_data=(
                        f"ref_premium_approve:{request_id}"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=(
                        f"ref_premium_reject:{request_id}"
                    )
                )
            ]
        ]
    )

@router.callback_query(F.data.startswith("payment_reject:"))
async def reject_payment_callback(
    callback: CallbackQuery,
    bot: Bot
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "❌ Siz admin emassiz!",
            show_alert=True
        )
        return

    payment_id = int(callback.data.split(":", 1)[1])

    payment = get_payment(payment_id)

    if not payment:
        await callback.answer(
            "❌ To'lov topilmadi!",
            show_alert=True
        )
        return

    if payment["status"] != "pending":
        await callback.answer(
            "⚠️ Bu to'lov allaqachon ko'rib chiqilgan.",
            show_alert=True
        )
        return

    reject_payment(
        payment_id,
        callback.from_user.id
    )

    try:
        await callback.message.edit_caption(
            caption=(
                callback.message.caption
                + "\n\n❌ <b>TO'LOV RAD ETILDI</b>"
            ),
            reply_markup=None
        )
    except Exception:
        pass

    await bot.send_message(
        payment["user_id"],
        "❌ <b>To'lovingiz tasdiqlanmadi.</b>\n\n"
        "Iltimos, to'lov ma'lumotlarini tekshirib, "
        "qaytadan urinib ko'ring."
    )

    await callback.answer(
        "❌ To'lov rad etildi."
    )


# ==========================================
# STATISTIKA
# ==========================================

@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):
    if not is_admin(message.from_user.id):
        return

    users_count = get_users_count()
    premium_count = get_premium_count()
    pending_count = get_pending_payments_count()

    await message.answer(
        "📊 <b>STATISTIKA</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{users_count}</b>\n"
        f"💎 Faol Premium: <b>{premium_count}</b>\n"
        f"⏳ Kutilayotgan to'lovlar: <b>{pending_count}</b>"
    )


# ==========================================
# PREMIUM FOYDALANUVCHILAR
# ==========================================

@router.message(F.text == "👥 Premium foydalanuvchilar")
async def premium_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = get_all_premium_users()

    if not users:
        await message.answer(
            "💎 Hozircha Premium foydalanuvchilar yo'q."
        )
        return

    text = "💎 <b>PREMIUM FOYDALANUVCHILAR</b>\n\n"

    for index, user in enumerate(users, start=1):
        username = (
            f"@{user['username']}"
            if user["username"]
            else "Username yo'q"
        )

        text += (
            f"{index}. 👤 {user['first_name'] or 'Nomsiz'}\n"
            f"   🆔 <code>{user['user_id']}</code>\n"
            f"   🔗 {username}\n\n"
        )

    # Telegram xabar limiti
    for i in range(0, len(text), 4000):
        await message.answer(text[i:i + 4000])


# ==========================================
# PREMIUMNI QO'LDA BERISH
# ==========================================

@router.message(F.text == "➕ Premium berish")
async def give_premium_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(
        AdminCourseState.waiting_manual_premium_user
    )

    await message.answer(
        "➕ <b>Premium berish</b>\n\n"
        "Foydalanuvchining Telegram ID raqamini yuboring.\n\n"
        "Masalan: <code>123456789</code>"
    )


@router.message(
    AdminCourseState.waiting_manual_premium_user
)
async def give_premium_user_id(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    if not is_admin(message.from_user.id):
        return

    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ ID faqat raqam bo'lishi kerak.\n"
            "Qaytadan yuboring:"
        )
        return

    activate_premium(user_id)

    await state.clear()

    await message.answer(
        f"✅ <code>{user_id}</code> foydalanuvchiga "
        "Premium berildi."
    )

    try:
        await bot.send_message(
            user_id,
            "🎉 Sizga admin tomonidan Premium berildi! 💎\n\n"
            "Endi barcha Premium kurslardan foydalanishingiz mumkin."
        )
    except Exception:
        pass


# ==========================================
# PREMIUMNI OLIB TASHLASH
# ==========================================

@router.message(F.text == "➖ Premiumni olib tashlash")
async def remove_premium_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(
        AdminCourseState.waiting_remove_premium_user
    )

    await message.answer(
        "➖ <b>Premiumni olib tashlash</b>\n\n"
        "Foydalanuvchining Telegram ID raqamini yuboring."
    )


@router.message(
    AdminCourseState.waiting_remove_premium_user
)
async def remove_premium_user_id(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    if not is_admin(message.from_user.id):
        return

    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ ID faqat raqam bo'lishi kerak."
        )
        return

    user = get_user_by_id(user_id)

    if not user:
        await message.answer(
            "❌ Bu ID bilan foydalanuvchi topilmadi."
        )
        return

    deactivate_premium(user_id)

    await state.clear()

    await message.answer(
        f"➖ <code>{user_id}</code> foydalanuvchining "
        "Premiumi o'chirildi."
    )

    try:
        await bot.send_message(
            user_id,
            "ℹ️ Sizning Premium obunangiz admin tomonidan "
            "faolsizlantirildi."
        )
    except Exception:
        pass


# ==========================================
# BO'LIM QO'SHISH
# ==========================================

@router.message(F.text == "➕ Bo'lim qo'shish")
async def add_section_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    courses = get_courses()

    await state.set_state(
        AdminCourseState.waiting_section_course
    )

    await message.answer(
        "📚 Qaysi kursga bo'lim qo'shamiz?",
        reply_markup=admin_courses_keyboard(
            courses,
            "admin_section_course"
        )
    )


@router.callback_query(
    F.data.startswith("admin_section_course:")
)
async def add_section_course_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        return

    course_id = int(callback.data.split(":", 1)[1])

    await state.update_data(course_id=course_id)

    await state.set_state(
        AdminCourseState.waiting_section_title
    )

    await callback.message.answer(
        "✍️ Yangi bo'lim nomini yuboring:"
    )

    await callback.answer()


@router.message(
    AdminCourseState.waiting_section_title
)
async def save_section(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    course_id = data["course_id"]

    from database import get_connection

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(position), 0) + 1
        FROM course_sections
        WHERE course_id=?
    """, (course_id,))

    position = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO course_sections (
            course_id,
            title,
            position
        )
        VALUES (?, ?, ?)
    """, (
        course_id,
        message.text.strip(),
        position
    ))

    conn.commit()
    conn.close()

    await state.clear()

    await message.answer(
        "✅ Bo'lim muvaffaqiyatli qo'shildi."
    )


# ==========================================
# BO'LIMNI O'CHIRISH
# ==========================================

@router.message(F.text == "🗑 Bo'limni o'chirish")
async def delete_section_start(message: Message):
    if not is_admin(message.from_user.id):
        return

    courses = get_courses()

    await message.answer(
        "🗑 Qaysi kursdan bo'lim o'chirmoqchisiz?",
        reply_markup=admin_courses_keyboard(
            courses,
            "delete_section_course"
        )
    )


@router.callback_query(
    F.data.startswith("delete_section_course:")
)
async def delete_section_course_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    course_id = int(callback.data.split(":", 1)[1])

    sections = get_sections(course_id)

    if not sections:
        await callback.answer(
            "Bu kursda bo'lim yo'q.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "O'chiriladigan bo'limni tanlang:",
        reply_markup=admin_sections_keyboard(
            sections,
            "delete_section"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("delete_section:")
)
async def delete_section_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    section_id = int(callback.data.split(":", 1)[1])

    section = get_section(section_id)

    if not section:
        await callback.answer(
            "Bo'lim topilmadi.",
            show_alert=True
        )
        return

    await callback.message.answer(
        f"⚠️ <b>{section['title']}</b> bo'limini o'chirmoqchimisiz?\n\n"
        "Ichidagi barcha video darslar ham o'chadi!",
        reply_markup=confirm_delete_section_keyboard(
            section_id
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("confirm_delete_section:")
)
async def confirm_delete_section(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    section_id = int(callback.data.split(":", 1)[1])

    delete_section(section_id)

    await callback.message.edit_text(
        "✅ Bo'lim va uning ichidagi video darslar o'chirildi."
    )

    await callback.answer()


# ==========================================
# VIDEO DARS QO'SHISH
# ==========================================

@router.message(F.text == "➕ Video dars qo'shish")
async def add_lesson_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    courses = get_courses()

    await message.answer(
        "📚 Avval kursni tanlang:",
        reply_markup=admin_courses_keyboard(
            courses,
            "admin_lesson_course"
        )
    )


@router.callback_query(
    F.data.startswith("admin_lesson_course:")
)
async def lesson_course_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    course_id = int(callback.data.split(":", 1)[1])

    sections = get_sections(course_id)

    if not sections:
        await callback.message.answer(
            "❌ Avval shu kursga bo'lim qo'shing."
        )
        await callback.answer()
        return

    await callback.message.answer(
        "📂 Bo'limni tanlang:",
        reply_markup=admin_sections_keyboard(
            sections,
            "admin_lesson_section"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("admin_lesson_section:")
)
async def lesson_section_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        return

    section_id = int(callback.data.split(":", 1)[1])

    await state.update_data(section_id=section_id)

    await state.set_state(
        AdminCourseState.waiting_lesson_title
    )

    await callback.message.answer(
        "✍️ Video dars nomini yuboring:"
    )

    await callback.answer()


@router.message(
    AdminCourseState.waiting_lesson_title
)
async def lesson_title(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.update_data(
        lesson_title=message.text.strip()
    )

    await state.set_state(
        AdminCourseState.waiting_lesson_video
    )

    await message.answer(
        "🎬 Endi video faylni yuboring:"
    )


@router.message(
    AdminCourseState.waiting_lesson_video,
    F.video
)
async def lesson_video(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.update_data(
        video_file_id=message.video.file_id
    )

    await state.set_state(
        AdminCourseState.waiting_lesson_description
    )

    await message.answer(
        "📝 Dars tavsifini yuboring.\n\n"
        "Kerak bo'lmasa: <code>yo'q</code>"
    )


@router.message(
    AdminCourseState.waiting_lesson_description
)
async def save_video_lesson(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    description = message.text.strip()

    if description.lower() in ["yo'q", "yoq"]:
        description = ""

    from database import get_connection

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(position), 0) + 1
        FROM video_lessons
        WHERE section_id=?
    """, (data["section_id"],))

    position = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO video_lessons (
            section_id,
            title,
            video_file_id,
            description,
            position
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["section_id"],
        data["lesson_title"],
        data["video_file_id"],
        description,
        position
    ))

    conn.commit()
    conn.close()

    await state.clear()

    await message.answer(
        "🎉 Video dars muvaffaqiyatli qo'shildi!"
    )


@router.message(
    AdminCourseState.waiting_lesson_video
)
async def wrong_video(message: Message):
    await message.answer(
        "❌ Iltimos, video fayl yuboring."
    )


# ==========================================
# VIDEO DARSNI O'CHIRISH
# ==========================================

@router.message(F.text == "🗑 Video darsni o'chirish")
async def delete_lesson_start(message: Message):
    if not is_admin(message.from_user.id):
        return

    courses = get_courses()

    await message.answer(
        "📚 Kursni tanlang:",
        reply_markup=admin_courses_keyboard(
            courses,
            "delete_lesson_course"
        )
    )


@router.callback_query(
    F.data.startswith("delete_lesson_course:")
)
async def delete_lesson_course_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    course_id = int(callback.data.split(":", 1)[1])

    sections = get_sections(course_id)

    if not sections:
        await callback.answer(
            "Bo'lim topilmadi.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "📂 Bo'limni tanlang:",
        reply_markup=admin_sections_keyboard(
            sections,
            "delete_lesson_section"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("delete_lesson_section:")
)
async def delete_lesson_section_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    section_id = int(callback.data.split(":", 1)[1])

    lessons = get_lessons(section_id)

    if not lessons:
        await callback.answer(
            "Bu bo'limda video dars yo'q.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "🎬 O'chiriladigan video darsni tanlang:",
        reply_markup=admin_lessons_keyboard(
            lessons,
            "delete_lesson"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("delete_lesson:")
)
async def delete_lesson_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    lesson_id = int(callback.data.split(":", 1)[1])

    lesson = get_lesson(lesson_id)

    if not lesson:
        await callback.answer(
            "Video dars topilmadi.",
            show_alert=True
        )
        return

    await callback.message.answer(
        f"⚠️ <b>{lesson['title']}</b> darsini o'chirmoqchimisiz?",
        reply_markup=confirm_delete_lesson_keyboard(
            lesson_id
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("confirm_delete_lesson:")
)
async def confirm_delete_lesson(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    lesson_id = int(callback.data.split(":", 1)[1])

    delete_lesson(lesson_id)

    await callback.message.edit_text(
        "✅ Video dars o'chirildi."
    )

    await callback.answer()


# ==========================================
# VIDEO DARSNI TAHRIRLASH
# ==========================================

@router.message(F.text == "✏️ Video darsni tahrirlash")
async def edit_lesson_start(message: Message):
    if not is_admin(message.from_user.id):
        return

    courses = get_courses()

    await message.answer(
        "📚 Kursni tanlang:",
        reply_markup=admin_courses_keyboard(
            courses,
            "edit_lesson_course"
        )
    )


@router.callback_query(
    F.data.startswith("edit_lesson_course:")
)
async def edit_lesson_course_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    course_id = int(callback.data.split(":", 1)[1])

    sections = get_sections(course_id)

    if not sections:
        await callback.answer(
            "Bo'lim topilmadi.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "📂 Bo'limni tanlang:",
        reply_markup=admin_sections_keyboard(
            sections,
            "edit_lesson_section"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("edit_lesson_section:")
)
async def edit_lesson_section_selected(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):
        return

    section_id = int(callback.data.split(":", 1)[1])

    lessons = get_lessons(section_id)

    if not lessons:
        await callback.answer(
            "Video dars topilmadi.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "🎬 Tahrirlanadigan darsni tanlang:",
        reply_markup=admin_lessons_keyboard(
            lessons,
            "edit_lesson"
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("edit_lesson:")
)
async def edit_lesson_selected(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        return

    lesson_id = int(callback.data.split(":", 1)[1])

    lesson = get_lesson(lesson_id)

    if not lesson:
        await callback.answer(
            "Dars topilmadi.",
            show_alert=True
        )
        return

    await state.update_data(edit_lesson_id=lesson_id)

    await state.set_state(
        AdminCourseState.waiting_edit_lesson_title
    )

    await callback.message.answer(
        f"✏️ Hozirgi nom:\n<b>{lesson['title']}</b>\n\n"
        "Yangi nomini yuboring:"
    )

    await callback.answer()


@router.message(
    AdminCourseState.waiting_edit_lesson_title
)
async def edit_lesson_title(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    update_lesson_title(
        data["edit_lesson_id"],
        message.text.strip()
    )

    await state.set_state(
        AdminCourseState.waiting_edit_lesson_description
    )

    await message.answer(
        "📝 Endi yangi tavsifini yuboring.\n\n"
        "Eski tavsifni o'chirish uchun: <code>yo'q</code>"
    )


@router.message(
    AdminCourseState.waiting_edit_lesson_description
)
async def edit_lesson_description(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    description = message.text.strip()

    if description.lower() in ["yo'q", "yoq"]:
        description = ""

    update_lesson_description(
        data["edit_lesson_id"],
        description
    )

    await state.set_state(
        AdminCourseState.waiting_edit_lesson_video
    )

    await message.answer(
        "🎬 Yangi video yuboring.\n\n"
        "Videoni o'zgartirmaslik uchun: <code>yo'q</code>"
    )


@router.message(
    AdminCourseState.waiting_edit_lesson_video,
    F.text.lower() == "yo'q"
)
@router.message(
    AdminCourseState.waiting_edit_lesson_video,
    F.text.lower() == "yoq"
)
async def skip_edit_video(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(
        "✅ Video dars muvaffaqiyatli tahrirlandi!"
    )


@router.message(
    AdminCourseState.waiting_edit_lesson_video,
    F.video
)
async def edit_lesson_video(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    update_lesson_video(
        data["edit_lesson_id"],
        message.video.file_id
    )

    await state.clear()

    await message.answer(
        "✅ Video dars muvaffaqiyatli tahrirlandi!"
    )


@router.message(
    AdminCourseState.waiting_edit_lesson_video
)
async def wrong_edit_video(message: Message):
    await message.answer(
        "❌ Video yuboring yoki <code>yo'q</code> deb yozing."
    )


# ==========================================
# HAMMAGA XABAR YUBORISH
# ==========================================

@router.message(F.text == "📢 Hammaga xabar")
async def broadcast_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.set_state(
        AdminCourseState.waiting_broadcast_message
    )

    await message.answer(
        "📢 <b>Hammaga xabar yuborish</b>\n\n"
        "Endi yubormoqchi bo'lgan xabaringizni jo'nating.\n\n"
        "Matn, rasm yoki video yuborishingiz mumkin."
    )


@router.message(
    AdminCourseState.waiting_broadcast_message
)
async def broadcast_message(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    if not is_admin(message.from_user.id):
        return

    users = get_all_users()

    await state.clear()

    success = 0
    failed = 0

    status_message = await message.answer(
        f"📢 Xabar yuborilmoqda...\n\n"
        f"👥 Jami: {len(users)}"
    )

    for user in users:
        try:
            await message.copy_to(
                chat_id=user["user_id"]
            )

            success += 1

        except Exception:
            failed += 1

        await asyncio.sleep(0.04)

    await status_message.edit_text(
        "✅ <b>XABAR YUBORISH TUGADI!</b>\n\n"
        f"📨 Yuborildi: {success}\n"
        f"❌ Yuborilmadi: {failed}"
    )


# ==========================================
# ADMIN ACTION BEKOR QILISH
# ==========================================

@router.callback_query(
    F.data == "cancel_admin_action"
)
async def cancel_admin_action(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_text(
        "❌ Amal bekor qilindi."
    )

    await callback.answer()
