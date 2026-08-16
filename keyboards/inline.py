from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def subscribe_keyboard(channel_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga a'zo bo'lish",
                    url=channel_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Tekshirish",
                    callback_data="check_subscription"
                )
            ]
        ]
    )


def premium_locked_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 To'lov qilish",
                    callback_data="payment_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Premium haqida tushuncha",
                    callback_data="premium_info"
                )
            ]
        ]
    )


def payment_methods_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Click",
                    callback_data="pay_click"
                ),
                InlineKeyboardButton(
                    text="🔵 Payme",
                    callback_data="pay_payme"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟠 Uzum Bank",
                    callback_data="pay_uzum"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="payment_back"
                )
            ]
        ]
    )


def admin_payment_keyboard(payment_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"payment_approve:{payment_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"payment_reject:{payment_id}"
                )
            ]
        ]
    )


def courses_keyboard(courses):
    keyboard = []

    for course in courses:
        keyboard.append([
            InlineKeyboardButton(
                text=course["title"],
                callback_data=f"course:{course['code']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def sections_keyboard(sections):
    keyboard = []

    for section in sections:
        keyboard.append([
            InlineKeyboardButton(
                text=section["title"],
                callback_data=f"section:{section['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def lessons_keyboard(lessons):
    keyboard = []

    for lesson in lessons:
        keyboard.append([
            InlineKeyboardButton(
                text=lesson["title"],
                callback_data=f"lesson:{lesson['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# =========================
# ADMIN KLAVIATURALARI
# =========================

def admin_courses_keyboard(courses, prefix: str):
    keyboard = []

    for course in courses:
        keyboard.append([
            InlineKeyboardButton(
                text=course["title"],
                callback_data=f"{prefix}:{course['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_sections_keyboard(sections, prefix: str):
    keyboard = []

    for section in sections:
        keyboard.append([
            InlineKeyboardButton(
                text=section["title"],
                callback_data=f"{prefix}:{section['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_lessons_keyboard(lessons, prefix: str):
    keyboard = []

    for lesson in lessons:
        keyboard.append([
            InlineKeyboardButton(
                text=lesson["title"],
                callback_data=f"{prefix}:{lesson['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def confirm_delete_section_keyboard(section_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Ha, o'chirish",
                    callback_data=f"confirm_delete_section:{section_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_admin_action"
                )
            ]
        ]
    )


def confirm_delete_lesson_keyboard(lesson_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Ha, o'chirish",
                    callback_data=f"confirm_delete_lesson:{lesson_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="cancel_admin_action"
                )
            ]
        ]
    )

def referral_link_keyboard(
    referral_link: str
):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Linkni nusxalash",
                    url=referral_link
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Ulashish",
                    url=(
                        "https://t.me/share/url"
                        f"?url={referral_link}"
                        "&text=Korean%20School%20Bot%20ga%20qo%27shiling!"
                    )
                )
            ]
        ]
    )
