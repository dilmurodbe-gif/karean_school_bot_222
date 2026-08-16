import sqlite3
from html import escape

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import ADMIN_ID

from database import (
    get_book_sections,
    get_book_section,
    create_book_section,
    delete_book_section,
    get_books_by_section,
    get_book,
    create_book,
    update_book,
    delete_book
)


router = Router()


# ============================================================
# VAQTINCHA HOLATLAR
# ============================================================

# user_id:
# ("section_new", None)
# ("book_new", section_id)
# ("edit", book_id)

waiting_book = {}


# ============================================================
# ADMIN TEKSHIRISH
# ============================================================

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ============================================================
# 📚 KITOB QO'SHISH
# ============================================================

@router.message(F.text == "📚 Kitob qo‘shish")
async def admin_books_start(message: Message):
    
    if not is_admin(message.from_user.id):
        return
        
        rows = get_book_sections()

        kb = InlineKeyboardMarkup(inline_keyboard=[])
    
        for section in rows[:40]:

                    kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"📁 {section['title']}",
                callback_data=f"bsec_{section['id']}"
            )
        ])
            

    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="➕ Yangi bo‘lim qo‘shish",
            callback_data="bsec_new"
        )
    ])

    await message.answer(
        "📚 Qaysi bo‘limga kitob qo‘shamiz?",
        reply_markup=kb
    )


# ============================================================
# ➕ YANGI BO'LIM
# ============================================================

@router.callback_query(F.data == "bsec_new")
async def bsec_new(callback: CallbackQuery):

    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Ruxsat yo‘q", show_alert=True)
        return

    waiting_book[callback.from_user.id] = (
        "section_new",
        None
    )

    await callback.message.answer(
        "➕ Yangi bo‘lim nomini yuboring.\n\n"
        "Masalan:\n"
        "서울대 한국어"
    )

    await callback.answer()


# ============================================================
# 💾 BO'LIMNI SAQLASH
# ============================================================

@router.message(
    lambda message:
        message.from_user.id in waiting_book
        and waiting_book[message.from_user.id][0] == "section_new"
)
async def bsec_save(message: Message):

    if not is_admin(message.from_user.id):
        return

    title = (message.text or "").strip()

    if not title:
        await message.answer(
            "❌ Bo‘lim nomi bo‘sh bo‘lmasin.\n"
            "Qayta yuboring."
        )
        return

    try:

        create_book_section(title)

    except sqlite3.IntegrityError:

        await message.answer(
            "⚠️ Bu bo‘lim allaqachon mavjud."
        )

        return

    waiting_book.pop(
        message.from_user.id,
        None
    )

    await message.answer(
        f"✅ Bo‘lim yaratildi:\n\n"
        f"📁 {escape(title)}\n\n"
        "Endi 📚 Kitob qo‘shish tugmasini bosing."
    )


# ============================================================
# 📁 BO'LIMNI OCHISH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bsec_")
        and callback.data.replace("bsec_", "").isdigit()
)
async def bsec_open(callback: CallbackQuery):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    section_id = int(
        callback.data.replace("bsec_", "")
    )

    section = get_book_section(section_id)

    if not section:
        await callback.message.answer(
            "❌ Bo‘lim topilmadi."
        )
        await callback.answer()
        return

    items = get_books_by_section(section_id)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[]
    )

    for book in items[:40]:

        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=f"📘 {book['title']}",
                callback_data=f"bedit_{book['id']}"
            )
        ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="➕ Yangi kitob qo‘shish",
            callback_data=f"bnew_{section_id}"
        )
    ])

    await callback.message.answer(
        f"📁 {escape(section['title'])}\n\n"
        "Kitobni tanlang yoki yangi kitob qo‘shing:",
        reply_markup=kb
    )

    await callback.answer()


# ============================================================
# ➕ YANGI KITOB
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bnew_")
        and callback.data.replace("bnew_", "").isdigit()
)
async def bnew(callback: CallbackQuery):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    section_id = int(
        callback.data.replace("bnew_", "")
    )

    section = get_book_section(section_id)

    if not section:
        await callback.message.answer(
            "❌ Bo‘lim topilmadi."
        )
        await callback.answer()
        return

    waiting_book[callback.from_user.id] = (
        "book_new",
        section_id
    )

    await callback.message.answer(
        "📘 <b>Yangi kitob qo‘shish</b>\n\n"
        "Quyidagi formatda yuboring:\n\n"
        "<code>nom=서울대 한국어 1</code>\n"
        "<code>matn=서울대 한국어 1 haqida ma'lumot</code>\n"
        "<code>kitob=https://...</code>\n"
        "<code>kanal=https://t.me/...</code>\n\n"
        "📌 <b>nom</b> — majburiy\n"
        "📌 <b>kitob</b> — majburiy\n"
        "📌 <b>matn</b> — ixtiyoriy\n"
        "📌 <b>kanal</b> — ixtiyoriy"
    )

    await callback.answer()


# ============================================================
# ✏️ KITOBNI TAHRIRLASH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bedit_")
        and callback.data.replace("bedit_", "").isdigit()
)
async def bedit(callback: CallbackQuery):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    book_id = int(
        callback.data.replace("bedit_", "")
    )

    book = get_book(book_id)

    if not book:
        await callback.message.answer(
            "❌ Kitob topilmadi."
        )
        await callback.answer()
        return

    waiting_book[callback.from_user.id] = (
        "edit",
        book_id
    )

    title = escape(book["title"])
    post_text = escape(book["post_text"] or "")
    book_link = escape(book["book_link"] or "")
    channel_link = escape(book["channel_link"] or "")

    await callback.message.answer(
        "✏️ <b>Kitobni tahrirlash</b>\n\n"
        "Quyidagi formatda qayta yuboring:\n\n"
        f"<code>nom={title}</code>\n"
        f"<code>matn={post_text}</code>\n"
        f"<code>kitob={book_link}</code>\n"
        f"<code>kanal={channel_link}</code>"
    )

    await callback.answer()


# ============================================================
# 💾 KITOBNI SAQLASH / TAHRIRLASH
# ============================================================

@router.message(
    lambda message:
        message.from_user.id in waiting_book
        and waiting_book[message.from_user.id][0]
        in ("book_new", "edit")
)
async def book_save_or_edit(message: Message):

    if not is_admin(message.from_user.id):
        return

    action, value = waiting_book[
        message.from_user.id
    ]

    text = (message.text or "").strip()

    if not text:
        await message.answer(
            "❌ Ma'lumot yuboring."
        )
        return

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    data = {}

    for line in lines:

        if "=" not in line:
            continue

        key, val = line.split("=", 1)

        data[key.strip().lower()] = val.strip()

    name = data.get("nom")
    post_text = data.get("matn", "")
    book_link = data.get("kitob", "")
    channel_link = data.get("kanal", "")

    # --------------------------------------------------------
    # MAJBURIY MAYDONLAR
    # --------------------------------------------------------

    if not name:
        await message.answer(
            "❌ <b>nom</b> majburiy.\n\n"
            "Masalan:\n"
            "<code>nom=서울대 한국어 1</code>"
        )
        return

    if not book_link:
        await message.answer(
            "❌ <b>kitob</b> linki majburiy.\n\n"
            "Masalan:\n"
            "<code>kitob=https://...</code>"
        )
        return

    # --------------------------------------------------------
    # YANGI KITOB
    # --------------------------------------------------------

    if action == "book_new":

        section_id = int(value)

        try:

            create_book(
                section_id=section_id,
                title=name,
                post_text=post_text,
                book_link=book_link,
                channel_link=channel_link
            )

        except sqlite3.IntegrityError:

            await message.answer(
                "⚠️ Shu bo‘limda bunday nomli kitob "
                "allaqachon mavjud.\n\n"
                "Kitob nomini o‘zgartiring."
            )

            return

        waiting_book.pop(
            message.from_user.id,
            None
        )

        await message.answer(
            f"✅ <b>Kitob qo‘shildi!</b>\n\n"
            f"📘 {escape(name)}"
        )

        return

    # --------------------------------------------------------
    # KITOBNI TAHRIRLASH
    # --------------------------------------------------------

    book_id = int(value)

    try:

        update_book(
            book_id=book_id,
            title=name,
            post_text=post_text,
            book_link=book_link,
            channel_link=channel_link
        )

    except sqlite3.IntegrityError:

        await message.answer(
            "⚠️ Shu bo‘limda bunday nomli kitob "
            "allaqachon mavjud."
        )

        return

    waiting_book.pop(
        message.from_user.id,
        None
    )

    await message.answer(
        f"✅ <b>Kitob yangilandi!</b>\n\n"
        f"📘 {escape(name)}"
    )


# ============================================================
# 📖 FOYDALANUVCHI — KITOBLAR
# ============================================================

@router.message(F.text == "📚 Kitoblar")
async def user_sections(message: Message):

    rows = get_book_sections()

    if not rows:

        await message.answer(
            "📭 Hozircha kitob bo‘limlari yo‘q."
        )
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"📁 {row['title']}",
                    callback_data=f"usec_{row['id']}"
                )
            ]
            for row in rows[:40]
        ]
    )

    await message.answer(
        "📚 <b>Bo‘lim tanlang:</b>",
        reply_markup=kb
    )


# ============================================================
# 📁 FOYDALANUVCHI — BO'LIM ICHIDAGI KITOBLAR
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("usec_")
        and callback.data.replace("usec_", "").isdigit()
)
async def user_books_in_section(
    callback: CallbackQuery
):

    section_id = int(
        callback.data.replace("usec_", "")
    )

    section = get_book_section(section_id)

    if not section:

        await callback.message.answer(
            "❌ Bo‘lim topilmadi."
        )

        await callback.answer()
        return

    items = get_books_by_section(
        section_id
    )

    if not items:

        await callback.message.answer(
            "📭 Bu bo‘limda kitoblar yo‘q."
        )

        await callback.answer()
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"📘 {book['title']}",
                    callback_data=f"ubook_{book['id']}"
                )
            ]
            for book in items[:50]
        ]
    )

    await callback.message.answer(
        f"📁 <b>{escape(section['title'])}</b>\n\n"
        "📘 Kitob tanlang:",
        reply_markup=kb
    )

    await callback.answer()


# ============================================================
# 📘 FOYDALANUVCHI — KITOBNI OCHISH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("ubook_")
        and callback.data.replace("ubook_", "").isdigit()
)
async def user_open_book(
    callback: CallbackQuery
):

    book_id = int(
        callback.data.replace("ubook_", "")
    )

    book = get_book(book_id)

    if not book:

        await callback.message.answer(
            "❌ Kitob topilmadi."
        )

        await callback.answer()
        return

    title = escape(book["title"])
    post_text = escape(
        book["post_text"] or ""
    )

    book_link = book["book_link"]
    channel_link = book["channel_link"]

    buttons = [
        [
            InlineKeyboardButton(
                text="📥 Kitobni olish",
                url=book_link
            )
        ]
    ]

    if channel_link:

        buttons.append([
            InlineKeyboardButton(
                text="📢 Kanalga o‘tish",
                url=channel_link
            )
        ])

    kb = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    text = (
        f"📘 <b>{title}</b>\n\n"
        f"{post_text or '📌 Kitob linki pastda 👇'}"
    )

    await callback.message.answer(
        text,
        reply_markup=kb
    )

    await callback.answer()


# ============================================================
# 🗑 KITOB O'CHIRISH
# ============================================================

@router.message(F.text == "🗑 Kitob o‘chirish")
async def admin_book_delete_start(
    message: Message
):

    if not is_admin(message.from_user.id):
        return

    rows = get_book_sections()

    if not rows:

        await message.answer(
            "📭 Hozircha bo‘limlar yo‘q."
        )
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"📁 {row['title']}",
                    callback_data=f"bdelsec_{row['id']}"
                )
            ]
            for row in rows[:50]
        ]
    )

    await message.answer(
        "🗑 <b>Qaysi bo‘limdagi kitobni o‘chiramiz?</b>",
        reply_markup=kb
    )


# ============================================================
# 🗑 O'CHIRISH — BO'LIM TANLASH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bdelsec_")
        and callback.data.replace("bdelsec_", "").isdigit()
)
async def admin_book_delete_choose(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    section_id = int(
        callback.data.replace("bdelsec_", "")
    )

    section = get_book_section(section_id)

    if not section:

        await callback.message.answer(
            "❌ Bo‘lim topilmadi."
        )

        await callback.answer()
        return

    items = get_books_by_section(
        section_id
    )

    if not items:

        await callback.message.answer(
            "📭 Bu bo‘limda kitob yo‘q."
        )

        await callback.answer()
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🗑 {book['title']}",
                    callback_data=f"bdel_{book['id']}"
                )
            ]
            for book in items[:80]
        ]
    )

    await callback.message.answer(
        f"📁 <b>{escape(section['title'])}</b>\n\n"
        "🗑 O‘chiriladigan kitobni tanlang:",
        reply_markup=kb
    )

    await callback.answer()


# ============================================================
# ⚠️ KITOB O'CHIRISH TASDIQLASH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bdel_")
        and callback.data.replace("bdel_", "").isdigit()
)
async def admin_book_delete_confirm(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    book_id = int(
        callback.data.replace("bdel_", "")
    )

    book = get_book(book_id)

    if not book:

        await callback.message.answer(
            "❌ Kitob topilmadi."
        )

        await callback.answer()
        return

    section = get_book_section(
        book["section_id"]
    )

    section_title = (
        section["title"]
        if section
        else "Noma'lum"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Yo‘q",
                    callback_data="bdel_cancel"
                ),
                InlineKeyboardButton(
                    text="✅ HA, O‘CHIRISH",
                    callback_data=f"bdel_yes_{book_id}"
                )
            ]
        ]
    )

    await callback.message.answer(
        "⚠️ <b>DIQQAT!</b>\n\n"
        f"📁 Bo‘lim: <b>{escape(section_title)}</b>\n"
        f"📘 Kitob: <b>{escape(book['title'])}</b>\n\n"
        "Haqiqatan o‘chirasizmi?",
        reply_markup=kb
    )

    await callback.answer()


# ============================================================
# ❌ KITOB O'CHIRISHNI BEKOR QILISH
# ============================================================

@router.callback_query(F.data == "bdel_cancel")
async def admin_book_delete_cancel(
    callback: CallbackQuery
):

    await callback.message.answer(
        "❌ Bekor qilindi."
    )

    await callback.answer()


# ============================================================
# ✅ KITOBNI O'CHIRISH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("bdel_yes_")
        and callback.data.replace("bdel_yes_", "").isdigit()
)
async def admin_book_delete_yes(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    book_id = int(
        callback.data.replace("bdel_yes_", "")
    )

    book = get_book(book_id)

    if not book:

        await callback.message.answer(
            "❌ Kitob topilmadi yoki allaqachon o‘chirilgan."
        )

        await callback.answer()
        return

    delete_book(book_id)

    await callback.message.answer(
        f"✅ Kitob o‘chirildi:\n"
        f"📘 {escape(book['title'])}"
    )

    await callback.answer()


# ============================================================
# 🗑 BO'LIM O'CHIRISH
# ============================================================

@router.message(F.text == "🗑 Bo‘lim o‘chirish")
async def admin_section_delete_start(
    message: Message
):

    if not is_admin(message.from_user.id):
        return

    rows = get_book_sections()

    if not rows:

        await message.answer(
            "📭 Bo‘limlar yo‘q."
        )
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🗑 {row['title']}",
                    callback_data=f"sdel_{row['id']}"
                )
            ]
            for row in rows[:80]
        ]
    )

    await message.answer(
        "🗑 <b>Qaysi bo‘limni o‘chiramiz?</b>",
        reply_markup=kb
    )


# ============================================================
# ⚠️ BO'LIM O'CHIRISH TASDIQLASH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("sdel_")
        and callback.data.replace("sdel_", "").isdigit()
)
async def admin_section_delete_confirm(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    section_id = int(
        callback.data.replace("sdel_", "")
    )

    section = get_book_section(
        section_id
    )

    if not section:

        await callback.message.answer(
            "❌ Bo‘lim topilmadi."
        )

        await callback.answer()
        return

    items = get_books_by_section(
        section_id
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Yo‘q",
                    callback_data="sdel_cancel"
                ),
                InlineKeyboardButton(
                    text="✅ HA, O‘CHIRISH",
                    callback_data=f"sdel_yes_{section_id}"
                )
            ]
        ]
    )

    if items:

        await callback.message.answer(
            "⚠️ <b>DIQQAT!</b>\n\n"
            f"📁 Bo‘lim: <b>{escape(section['title'])}</b>\n"
            f"📘 Ichida {len(items)} ta kitob bor.\n\n"
            "Bo‘lim va uning ichidagi barcha "
            "kitoblar o‘chiriladi.\n\n"
            "Haqiqatan o‘chirasizmi?",
            reply_markup=kb
        )

    else:

        await callback.message.answer(
            "⚠️ <b>DIQQAT!</b>\n\n"
            f"📁 Bo‘lim: <b>{escape(section['title'])}</b>\n\n"
            "Haqiqatan o‘chirasizmi?",
            reply_markup=kb
        )

    await callback.answer()


# ============================================================
# ❌ BO'LIM O'CHIRISHNI BEKOR QILISH
# ============================================================

@router.callback_query(F.data == "sdel_cancel")
async def sdel_cancel(
    callback: CallbackQuery
):

    await callback.message.answer(
        "❌ Bekor qilindi."
    )

    await callback.answer()


# ============================================================
# ✅ BO'LIMNI O'CHIRISH
# ============================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("sdel_yes_")
        and callback.data.replace("sdel_yes_", "").isdigit()
)
async def sdel_yes(
    callback: CallbackQuery
):

    if not is_admin(callback.from_user.id):
        await callback.answer(
            "⛔ Ruxsat yo‘q",
            show_alert=True
        )
        return

    section_id = int(
        callback.data.replace("sdel_yes_", "")
    )

    section = get_book_section(
        section_id
    )

    if not section:

        await callback.message.answer(
            "❌ Bo‘lim topilmadi yoki allaqachon o‘chirilgan."
        )

        await callback.answer()
        return

    title = section["title"]

    # ON DELETE CASCADE
    # ichidagi barcha kitoblar ham o'chadi
    delete_book_section(section_id)

    await callback.message.answer(
        f"✅ Bo‘lim o‘chirildi:\n"
        f"📁 {escape(title)}\n\n"
        "📘 Ichidagi kitoblar ham o‘chirildi."
    )

    await callback.answer()
  
