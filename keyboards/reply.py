from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def mode_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Oddiy"),
                KeyboardButton(text="💎 Premium")
            ],
            [
                KeyboardButton(text="ℹ️ Bot haqida")
            ],
            [
                KeyboardButton(
                    text="💎 Premium haqida to'liq tushuncha"
                )
            ],
        ],

        resize_keyboard=True
    )


def ordinary_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Kitoblar"),
                KeyboardButton(text="🔤 Harflar")
            ],
            [
                KeyboardButton(text="📘 Grammatikalar"),
                KeyboardButton(text="📅 Bugungi grammatika")
            ],
            [
                KeyboardButton(text="💬 Chatimiz"),
                KeyboardButton(text="📞 Aloqa")
            ],
            [
                KeyboardButton(text="🏠 Bo'lim tanlash")
            ]
        ],
        resize_keyboard=True

    )


def premium_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌱 Boshlang'ich")
            ],
            [
                KeyboardButton(text="🥉 TOPIK 1"),
                KeyboardButton(text="🥇 TOPIK 2")
            ],
            [
                KeyboardButton(text="🎙 Podcast / VD")
            ],
            [
                KeyboardButton(text="🤖 AI Teacher")
            ],
            [
                KeyboardButton(text="🏠 Bo'lim tanlash")
            ]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="📢 Hammaga xabar")
            ],
            [
                KeyboardButton(text="👥 Premium foydalanuvchilar")
            ],
            [
                KeyboardButton(text="➕ Bo'lim qo'shish"),
                KeyboardButton(text="🗑 Bo'limni o'chirish")
            ],
            [
                KeyboardButton(text="➕ Video dars qo'shish")
            ],
            [
                KeyboardButton(text="✏️ Video darsni tahrirlash"),
                KeyboardButton(text="🗑 Video darsni o'chirish")
            ],
            [
                KeyboardButton(text="➕ Premium berish"),
                KeyboardButton(text="➖ Premiumni olib tashlash")
            ],
            [
                KeyboardButton(text="➕ Bugungi grammatikani qo‘shish"),
                KeyboardButton(text="❌ Bugungi grammatikani o‘chirish"),
            ],
            [
                KeyboardButton(text="➕ Podcast qo‘shish"),
                KeyboardButton(text="🗑 Podcast o'chirish")
            ],
            [
                KeyboardButton(text="📋 Podcastlar ro'yxati")
            ],
            [
                KeyboardButton(text="📚 Kitob qo‘shish"),
                KeyboardButton(text="📖 Kitoblar")
            ],
            [
                KeyboardButton(text="🗑 Kitob o‘chirish"),
                KeyboardButton(text="🗑 Bo‘lim o‘chirish")
            ],
            [
                KeyboardButton(text="🏠 Bo'lim tanlash")
            ]
        ],
        resize_keyboard=True
    )
