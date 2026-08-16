from aiogram import Router, F
from aiogram.types import Message

from config import CONTACT, CHAT_LINK
from keyboards.reply import ordinary_menu, mode_menu


router = Router()


@router.message(F.text == "📚 Oddiy")
async def ordinary_section(message: Message):
    await message.answer(
        "📚 Oddiy bo'limga xush kelibsiz!\n\n"
        "Bu bo'limdagi materiallardan bepul foydalanishingiz mumkin.",
        reply_markup=ordinary_menu()
    )


@router.message(F.text == "🏠 Bo'lim tanlash")
async def choose_section(message: Message):
    await message.answer(
        "Qaysi bo'limga kirmoqchisiz? 👇",
        reply_markup=mode_menu()
    )

@router.message(F.text == "💬 Chatimiz")
async def chat(message: Message):
    if CHAT_LINK:
        await message.answer(
            f"💬 Chatimizga qo'shiling:\n{CHAT_LINK}"
        )
    else:
        await message.answer(
            "💬 Chatimiz havolasi hali sozlanmagan."
        )


@router.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer(
        f"📞 Aloqa uchun:\n{CONTACT}"
    )


@router.message(F.text == "💎 Premium haqida to'liq tushuncha")
@router.message(F.text == "💳 Premium haqida")
async def premium_full_info(message: Message):
    await message.answer(
        "💎 <b>PREMIUM HAQIDA</b>\n\n"

        "Premium obuna orqali botdagi barcha premium bo‘limlardan "
        "foydalanish imkoniyatiga ega bo‘lasiz! 🚀\n\n"

        "📚 <b>PREMIUM KURSLAR:</b>\n\n"
        "🌱 Boshlang‘ich kurs\n"
        "🥉 TOPIK 1 kursi\n"
        "🥇 TOPIK 2 kursi\n\n"

        "🎬 <b>VIDEO DARSLAR</b>\n"
        "Har bir kurs uchun tayyorlangan foydali va tushunarli "
        "video darslardan foydalanishingiz mumkin.\n\n"

        "🎙 <b>PODCASTLAR</b>\n"
        "Koreys tilini tinglash va tushunish ko‘nikmangizni "
        "rivojlantirish uchun maxsus podcastlardan foydalaning.\n\n"

        "🤖 <b>AI TEACHER</b>\n"
        "Tushunmagan savollaringizni AI Teacher orqali so‘rashingiz "
        "va qo‘shimcha yordam olishingiz mumkin. 💬\n\n"

        "✨ <b>VA YANA KO‘PLAB IMKONIYATLAR</b>\n"
        "Premium bo‘limiga doimiy ravishda yangi darslar, foydali "
        "materiallar va yangi funksiyalar qo‘shib borilmoqda! 🔥\n\n"

        "💎 Premium sotib olganingizdan so‘ng bitta obuna orqali "
        "barcha premium kurslar va imkoniyatlardan foydalanish "
        "huquqiga ega bo‘lasiz.\n\n"

        "🚀 <b>Korean School bilan koreys tilini yanada osonroq "
        "o‘rganishni boshlang!</b>"
    )


@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    await message.answer(
        "ℹ️ <b>KOREAN SCHOOL HAQIDA</b>\n\n"

        "🇰🇷 <b>Korean School</b> — koreys tilini "
        "o‘rganishingiz uchun yaratilgan ta’limiy bot.\n\n"

        "📚 <b>Kitoblar</b>\n"
        "Koreys tili bo‘yicha foydali darslik va o‘quv "
        "materiallaridan foydalanishingiz mumkin.\n\n"

        "🔤 <b>Harflar</b>\n"
        "Koreys alifbosi — Hangul harflarini o‘rganish, "
        "ularning talaffuzi va qo‘llanilishini ko‘rib chiqish mumkin.\n\n"

        "📘 <b>Grammatikalar</b>\n"
        "Koreys tilidagi grammatikalarni bosqichma-bosqich "
        "o‘rganishingiz mumkin.\n\n"

        "📅 <b>Bugungi grammatika</b>\n"
        "Har kuni yangi grammatika va foydali mavzularni "
        "o‘rganib borishingiz mumkin. ✨\n\n"

        "💬 <b>Chatimiz</b>\n"
        "Boshqa o‘rganuvchilar bilan muloqot qilish va "
        "koreys tili bo‘yicha fikr almashish imkoniyati mavjud.\n\n"

        "📞 <b>Aloqa</b>\n"
        "Savol, taklif yoki muammo bo‘lsa, biz bilan bog‘lanishingiz mumkin.\n\n"

        "💎 <b>Premium</b>\n"
        "Premium orqali yanada ko‘proq kurslar, video darslar, "
        "podcastlar, AI Teacher va boshqa qo‘shimcha imkoniyatlardan "
        "foydalanishingiz mumkin. 🚀\n\n"

        "💡 <b>Premium haqida to‘liq ma’lumot olish uchun</b>\n"
        "💎 <b>«Premium haqida to'liq tushuncha»</b> tugmasini bosing.\n\n"

        "🔥 Botga doimiy ravishda yangi darslar, materiallar "
        "va foydali funksiyalar qo‘shib borilmoqda!\n\n"

        "🇰🇷 <b>Korean School — koreys tilini o‘rganishni "
        "osonroq va qiziqarliroq qilamiz!</b>"
    )
