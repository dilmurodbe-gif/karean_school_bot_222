from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()


# ==========================================
# HARFLAR MA'LUMOTLARI
# ==========================================

hangeul_letters_data = {
    "ㄱ": "🔊 Talaffuz: ㄱ (g/k)\nGap boshida k, ichida g kabi\n\n🇰🇷 Misol: 고기\n🗣 Talaffuzi: gogi\n🇺🇿 Tarjima: go‘sht",
    "ㄲ": "🔊 Talaffuz: ㄲ (kk)\nKuchli k tovushi\n\n🇰🇷 Misol: 끼다\n🗣 Talaffuzi: kkida\n🇺🇿 Tarjima: kiymoq",
    "ㄴ": "🔊 Talaffuz: ㄴ (n)\nDoimo n kabi\n\n🇰🇷 Misol: 누구\n🗣 Talaffuzi: dugu\n🇺🇿 Tarjima: kim?",
    "ㄷ": "🔊 Talaffuz: ㄷ (d/t)\nBoshida t, ichida d\n\n🇰🇷 Misol: 다리\n🗣 Talaffuzi: dari\n🇺🇿 Tarjima: oyoq / ko‘prik",
    "ㄸ": "🔊 Talaffuz: ㄸ (tt)\nKuchli t tovushi\n\n🇰🇷 Misol: 땅\n🗣 Talaffuzi: ttang\n🇺🇿 Tarjima: yer",
    "ㄹ": "🔊 Talaffuz: ㄹ (r/l)\nBoshida r, oxirida yoki undoshdan keyin l\n\n🇰🇷 Misol: 사람\n🗣 Talaffuzi: saram\n🇺🇿 Tarjima: inson",
    "ㅁ": "🔊 Talaffuz: ㅁ (m)\nM tovushi\n\n🇰🇷 Misol: 머리\n🗣 Talaffuzi: mori\n🇺🇿 Tarjima: bosh",
    "ㅂ": "🔊 Talaffuz: ㅂ (b/p)\nBoshida p, ichida b\n\n🇰🇷 Misol: 바지\n🗣 Talaffuzi: paji\n🇺🇿 Tarjima: shim",
    "ㅃ": "🔊 Talaffuz: ㅃ (pp)\nKuchli p tovushi\n\n🇰🇷 Misol: 빵\n🗣 Talaffuzi: ppang\n🇺🇿 Tarjima: non",
    "ㅅ": "🔊 Talaffuz: ㅅ (s)\nI bilan yumshoq eshitiladi\n\n🇰🇷 Misol: 사과\n🗣 Talaffuzi: sagwa\n🇺🇿 Tarjima: olma",
    "ㅆ": "🔊 Talaffuz: ㅆ (ss)\nKuchli s tovushi\n\n🇰🇷 Misol: 쌀\n🗣 Talaffuzi: ssal\n🇺🇿 Tarjima: guruch",
    "ㅇ": "🔊 Talaffuz: ㅇ (ng)\nBoshida aytilmaydi, oxirida ng sifatida\n\n🇰🇷 Misol: 아이\n🗣 Talaffuzi: ai\n🇺🇿 Tarjima: bola",
    "ㅈ": "🔊 Talaffuz: ㅈ (j)\nJ tovushi\n\n🇰🇷 Misol: 자전거\n🗣 Talaffuzi: jajŏngŏ\n🇺🇿 Tarjima: velosiped",
    "ㅉ": "🔊 Talaffuz: ㅉ (jj)\nKuchli j tovushi\n\n🇰🇷 Misol: 짜다\n🗣 Talaffuzi: jjada\n🇺🇿 Tarjima: sho‘r",
    "ㅊ": "🔊 Talaffuz: ㅊ (ch)\nCh tovushi\n\n🇰🇷 Misol: 친구\n🗣 Talaffuzi: chinggu\n🇺🇿 Tarjima: do‘st",
    "ㅋ": "🔊 Talaffuz: ㅋ (k)\nKuchli k\n\n🇰🇷 Misol: 코\n🗣 Talaffuzi: ko\n🇺🇿 Tarjima: burun",
    "ㅌ": "🔊 Talaffuz: ㅌ (t)\nKuchli t\n\n🇰🇷 Misol: 토끼\n🗣 Talaffuzi: tokki\n🇺🇿 Tarjima: quyon",
    "ㅍ": "🔊 Talaffuz: ㅍ (p)\nKuchli p\n\n🇰🇷 Misol: 포도\n🗣 Talaffuzi: podo\n🇺🇿 Tarjima: uzum",
    "ㅎ": "🔊 Talaffuz: ㅎ (h)\nH tovushi\n\n🇰🇷 Misol: 하나\n🗣 Talaffuzi: hana\n🇺🇿 Tarjima: bir",

    "ㅏ": "🔊 Talaffuz: ㅏ (a)\nOg‘iz katta ochiladi\n\n🇰🇷 Misol: 아빠\n🗣 Talaffuzi: appa\n🇺🇿 Tarjima: dada",
    "ㅐ": "🔊 Talaffuz: ㅐ (ae)\nE ga o‘xshash\n\n🇰🇷 Misol: 개\n🗣 Talaffuzi: ke\n🇺🇿 Tarjima: it",
    "ㅑ": "🔊 Talaffuz: ㅑ (ya)\nYa tovushi\n\n🇰🇷 Misol: 야채\n🗣 Talaffuzi: yachae\n🇺🇿 Tarjima: sabzavot",
    "ㅒ": "🔊 Talaffuz: ㅒ (yae)\nYa + e\n\n🇰🇷 Misol: 얘기\n🗣 Talaffuzi: yaegi\n🇺🇿 Tarjima: suhbat",
    "ㅓ": "🔊 Talaffuz: ㅓ (eo)\nO ga o‘xshash, orqadan chiqadi\n\n🇰🇷 Misol: 어머니\n🗣 Talaffuzi: ŏmŏni\n🇺🇿 Tarjima: ona",
    "ㅔ": "🔊 Talaffuz: ㅔ (e)\nInglizcha e kabi\n\n🇰🇷 Misol: 네\n🗣 Talaffuzi: ne\n🇺🇿 Tarjima: ha",
    "ㅕ": "🔊 Talaffuz: ㅕ (yeo)\nYo ga o‘xshash\n\n🇰🇷 Misol: 여자\n🗣 Talaffuzi: yŏja\n🇺🇿 Tarjima: ayol",
    "ㅖ": "🔊 Talaffuz: ㅖ (ye)\nYe tovushi\n\n🇰🇷 Misol: 예\n🗣 Talaffuzi: ye\n🇺🇿 Tarjima: ha (hurmatli)",
    "ㅗ": "🔊 Talaffuz: ㅗ (o)\nYuqoriga qarab o\n\n🇰🇷 Misol: 오이\n🗣 Talaffuzi: oi\n🇺🇿 Tarjima: bodring",
    "ㅘ": "🔊 Talaffuz: ㅘ (wa)\nO + a\n\n🇰🇷 Misol: 사과\n🗣 Talaffuzi: sagwa\n🇺🇿 Tarjima: olma",
    "ㅙ": "🔊 Talaffuz: ㅙ (wae)\nO + ae\n\n🇰🇷 Misol: 왜\n🗣 Talaffuzi: wae\n🇺🇿 Tarjima: nega",
    "ㅚ": "🔊 Talaffuz: ㅚ (oe)\nWe yoki ö kabi\n\n🇰🇷 Misol: 외국\n🗣 Talaffuzi: oeguk\n🇺🇿 Tarjima: chet el",
    "ㅛ": "🔊 Talaffuz: ㅛ (yo)\nYuqoriga qarab yo\n\n🇰🇷 Misol: 요리\n🗣 Talaffuzi: yori\n🇺🇿 Tarjima: taom",
    "ㅜ": "🔊 Talaffuz: ㅜ (u)\nPastga qarab u\n\n🇰🇷 Misol: 우유\n🗣 Talaffuzi: uyu\n🇺🇿 Tarjima: sut",
    "ㅝ": "🔊 Talaffuz: ㅝ (wo)\nU + eo\n\n🇰🇷 Misol: 워터\n🗣 Talaffuzi: wŏtŏ\n🇺🇿 Tarjima: suv",
    "ㅞ": "🔊 Talaffuz: ㅞ (we)\nU + e\n\n🇰🇷 Misol: 웨딩\n🗣 Talaffuzi: weding\n🇺🇿 Tarjima: to‘y",
    "ㅟ": "🔊 Talaffuz: ㅟ (wi)\nU + i\n\n🇰🇷 Misol: 위\n🗣 Talaffuzi: wi\n🇺🇿 Tarjima: usti",
    "ㅠ": "🔊 Talaffuz: ㅠ (yu)\nPastga qarab yu\n\n🇰🇷 Misol: 유리\n🗣 Talaffuzi: yuri\n🇺🇿 Tarjima: oyna",
    "ㅡ": "🔊 Talaffuz: ㅡ (eu)\nOg‘iz tekis\n\n🇰🇷 Misol: 으깨다\n🗣 Talaffuzi: ukkæda\n🇺🇿 Tarjima: ezmoq",
    "ㅢ": "🔊 Talaffuz: ㅢ (ui)\nEu + i\n\n🇰🇷 Misol: 의사\n🗣 Talaffuzi: ŭisa\n🇺🇿 Tarjima: shifokor",
    "ㅣ": "🔊 Talaffuz: ㅣ (i)\nI tovushi\n\n🇰🇷 Misol: 이름\n🗣 Talaffuzi: irŭm\n🇺🇿 Tarjima: ism"
}


# ==========================================
# HARFLAR MENYUSI
# ==========================================

def letters_keyboard():
    markup = InlineKeyboardMarkup(inline_keyboard=[])

    row = []

    for i, harf in enumerate(hangeul_letters_data.keys(), start=1):
        row.append(
            InlineKeyboardButton(
                text=harf,
                callback_data=f"harf:{harf}"
            )
        )

        if i % 4 == 0:
            markup.inline_keyboard.append(row)
            row = []

    if row:
        markup.inline_keyboard.append(row)

    markup.inline_keyboard.append([
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data="letters_close"
        )
    ])

    return markup


# ==========================================
# 🔤 HARFLAR TUGMASI
# ==========================================

@router.message(F.text == "🔤 Harflar")
async def show_letter_menu(message: Message):
    await message.answer(
        "🇰🇷 <b>HANGEUL — KOREYS ALIFBOSI</b>\n\n"
        "O'rganmoqchi bo'lgan harfni tanlang 👇",
        reply_markup=letters_keyboard()
    )


# ==========================================
# HARFNI KO'RSATISH
# ==========================================

@router.callback_query(F.data.startswith("harf:"))
async def show_letter(callback: CallbackQuery):
    harf = callback.data.split(":", 1)[1]

    info = hangeul_letters_data.get(harf)

    if not info:
        await callback.answer(
            "❌ Harf topilmadi!",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        f"🇰🇷 <b>{harf}</b>\n\n"
        f"{info}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Harflar",
                        callback_data="letters_menu"
                    )
                ]
            ]
        )
    )

    await callback.answer()


# ==========================================
# HARFLAR MENYUSIGA QAYTISH
# ==========================================

@router.callback_query(F.data == "letters_menu")
async def back_to_letters(callback: CallbackQuery):
    await callback.message.edit_text(
        "🇰🇷 <b>HANGEUL — KOREYS ALIFBOSI</b>\n\n"
        "O'rganmoqchi bo'lgan harfni tanlang 👇",
        reply_markup=letters_keyboard()
    )

    await callback.answer()


# ==========================================
# YOPISH
# ==========================================

@router.callback_query(F.data == "letters_close")
async def close_letters(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
