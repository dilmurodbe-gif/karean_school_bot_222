from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    get_all_podcasts,
    get_podcast,
    add_podcast,
    delete_podcast
)

from config import ADMIN_ID


router = Router()

# Admin podcast qo'shish holati
admin_state = {}

# Podcast o'chirish holati
delete_state = {}


# ================== PODCAST KEYBOARD ==================

def get_podcast_keyboard():

    podcasts = get_all_podcasts()

    keyboard = []

    for pid, data in podcasts.items():

        keyboard.append([
            InlineKeyboardButton(
                text=f"🎙 {data['title']}",
                callback_data=f"pod_view_{pid}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


# ================== ADMIN TEKSHIRISH ==================

def is_admin(user_id: int):
    return user_id == ADMIN_ID


# ================== OPEN PODCAST MENU ==================

@router.message(F.text == "🎙 Podcast / VD")
async def open_podcast(message: Message):

    podcasts = get_all_podcasts()

    if not podcasts:
        await message.answer("❌ Hozircha podcast yo‘q")
        return

    await message.answer(
        "🎙 <b>Podcastlar:</b>",
        reply_markup=get_podcast_keyboard()
    )


# ================== VIEW PODCAST ==================

@router.callback_query(F.data.startswith("pod_view_"))
async def view_podcast(callback: CallbackQuery):

    pid = int(callback.data.split("_")[2])

    data = get_podcast(pid)

    if not data:
        await callback.message.answer("❌ Podcast topilmadi")
        await callback.answer()
        return

    await callback.message.answer(
        f"🎙 <b>{data['title']}</b>"
    )

    # VIDEO
    if data.get("video"):

        await callback.message.answer_video(
            data["video"]
        )

    # PDF
    if data.get("pdf"):

        await callback.message.answer_document(
            data["pdf"]
        )

    else:
        await callback.message.answer(
            "📄 Bu podcast uchun PDF yo‘q"
        )

    await callback.answer()


# ================== ADD PODCAST START ==================

@router.message(F.text == "➕ Podcast qo‘shish")
async def add_start(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz")
        return

    admin_state[message.from_user.id] = {
        "step": 1
    }

    await message.answer(
        "🔢 Yangi Podcast ID sini kiriting:\n\n"
        "Masalan: <code>1</code>"
    )


# ================== DELETE START ==================

@router.message(F.text == "🗑 Podcast o'chirish")
async def delete_start(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz")
        return

    delete_state[message.from_user.id] = True

    await message.answer(
        "🔢 O‘chiriladigan Podcast ID sini yuboring:"
    )


# ================== PODCAST LIST ==================

@router.message(F.text == "📋 Podcastlar ro'yxati")
async def list_podcasts(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz")
        return

    podcasts = get_all_podcasts()

    if not podcasts:
        await message.answer("❌ Hozircha podcast yo‘q")
        return

    text = "📋 <b>PODCASTLAR RO‘YXATI:</b>\n\n"

    for pid, data in podcasts.items():
        text += f"🔢 <b>ID {pid}</b> — {data['title']}\n"

    await message.answer(text)


# ================== ADMIN FLOW ==================

@router.message()
async def podcast_admin_flow(message: Message):

    user_id = message.from_user.id

    # ================== ADD FLOW ==================

    if user_id in admin_state:

        state = admin_state[user_id]
        step = state["step"]

        # STEP 1 = ID
        if step == 1:

            if not message.text or not message.text.isdigit():

                await message.answer(
                    "❌ ID faqat raqam bo‘lishi kerak"
                )
                return

            pid = int(message.text)

            # Shu ID oldindan mavjudligini tekshirish
            if get_podcast(pid):

                await message.answer(
                    "❌ Bu ID bilan Podcast allaqachon mavjud!\n\n"
                    "Boshqa ID kiriting:"
                )
                return

            state["id"] = pid
            state["step"] = 2

            await message.answer(
                "📌 Podcast nomini yuboring:"
            )
            return

        # STEP 2 = TITLE
        if step == 2:

            if not message.text:

                await message.answer(
                    "❌ Podcast nomini matn shaklida yuboring"
                )
                return

            state["title"] = message.text
            state["step"] = 3

            await message.answer(
                "🎥 Endi Podcast videosini yuboring:"
            )
            return

        # STEP 3 = VIDEO
        if step == 3:

            if not message.video:

                await message.answer(
                    "❌ Iltimos, video yuboring"
                )
                return

            # Telegram file_id saqlaymiz
            state["video"] = message.video.file_id
            state["step"] = 4

            await message.answer(
                "📄 PDF yuboring.\n\n"
                "Agar PDF bo‘lmasa: <code>yo'q</code> deb yozing."
            )
            return

        # STEP 4 = PDF
        if step == 4:

            pdf = None

            if message.document:
                pdf = message.document.file_id

            elif (
                message.text
                and message.text.lower() in ["yo'q", "yoq", "yo‘q"]
            ):
                pdf = None

            else:

                await message.answer(
                    "❌ PDF yuboring yoki <code>yo'q</code> deb yozing."
                )
                return

            add_podcast(
                state["id"],
                state["title"],
                state["video"],
                pdf
            )

            await message.answer(
                "✅ <b>Podcast muvaffaqiyatli saqlandi!</b>\n\n"
                f"🔢 ID: {state['id']}\n"
                f"📌 Nomi: {state['title']}"
            )

            del admin_state[user_id]

            return

    # ================== DELETE FLOW ==================

    if user_id in delete_state:

        if not message.text or not message.text.isdigit():

            await message.answer(
                "❌ ID raqam bo‘lishi kerak"
            )
            return

        pid = int(message.text)

        data = get_podcast(pid)

        if not data:

            await message.answer(
                "❌ Bunday Podcast topilmadi"
            )

            del delete_state[user_id]
            return

        delete_podcast(pid)

        await message.answer(
            "🗑 <b>Podcast o‘chirildi!</b>\n\n"
            f"📌 {data['title']}"
        )

        del delete_state[user_id]

        return
