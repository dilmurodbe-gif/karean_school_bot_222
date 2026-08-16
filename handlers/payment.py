from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import (
    PREMIUM_PRICE,
    CLICK_INFO,
    PAYME_INFO,
    UZUM_INFO,
    ADMIN_ID
)

from states import PaymentState

from database import (
    get_pending_payment_by_user,
    create_payment
)

from keyboards.inline import (
    payment_methods_keyboard,
    premium_locked_keyboard,
    admin_payment_keyboard
)


router = Router()


@router.callback_query(F.data == "payment_start")
async def payment_start(callback: CallbackQuery):
    pending = get_pending_payment_by_user(
        callback.from_user.id
    )

    if pending:
        await callback.answer(
            "Sizning oldingi to'lovingiz hali tekshirilmoqda.",
            show_alert=True
        )
        return

    await callback.message.answer(
        "💳 PREMIUM TO'LOV\n\n"
        "Bitta Premium obunasi bilan:\n\n"
        "🌱 Boshlang'ich\n"
        "🥉 TOPIK 1\n"
        "🥇 TOPIK 2\n\n"
        "kurslarining barcha video darslari ochiladi.\n\n"
        f"💰 Narxi: {PREMIUM_PRICE} so'm\n\n"
        "To'lov usulini tanlang 👇",
        reply_markup=payment_methods_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "payment_back")
async def payment_back(callback: CallbackQuery):
    await callback.message.answer(
        "Premium haqida ma'lumot:",
        reply_markup=premium_locked_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "premium_info")
async def premium_info(callback: CallbackQuery):
    await callback.message.answer(
        "💎 PREMIUM HAQIDA TO'LIQ MA'LUMOT\n\n"
        "Premium sotib olganingizdan keyin barcha kurslar "
        "bir vaqtda ochiladi:\n\n"
        "🌱 Boshlang'ich\n"
        "🥉 TOPIK 1\n"
        "🥇 TOPIK 2\n\n"
        "🎬 Barcha video darslarga kirish huquqi beriladi.\n\n"
        f"💰 Premium narxi: {PREMIUM_PRICE} so'm"
    )

    await callback.answer()


async def select_payment(
    callback: CallbackQuery,
    state: FSMContext,
    method: str,
    info: str
):
    await state.update_data(payment_method=method)

    await state.set_state(
        PaymentState.waiting_receipt
    )

    await callback.message.answer(
        f"💳 {method} orqali to'lov\n\n"
        f"💰 To'lov summasi: {PREMIUM_PRICE} so'm\n\n"
        f"📌 To'lov ma'lumotlari:\n{info}\n\n"
        "━━━━━━━━━━━━━━\n"
        "🧾 To'lovni amalga oshirgach, "
        "chek rasmini yoki PDF faylini shu chatga yuboring.\n\n"
        "Admin tekshirganidan keyin Premium faollashadi."
    )

    await callback.answer()


@router.callback_query(F.data == "pay_click")
async def pay_click(callback: CallbackQuery, state: FSMContext):
    await select_payment(
        callback,
        state,
        "Click",
        CLICK_INFO
    )


@router.callback_query(F.data == "pay_payme")
async def pay_payme(callback: CallbackQuery, state: FSMContext):
    await select_payment(
        callback,
        state,
        "Payme",
        PAYME_INFO
    )


@router.callback_query(F.data == "pay_uzum")
async def pay_uzum(callback: CallbackQuery, state: FSMContext):
    await select_payment(
        callback,
        state,
        "Uzum Bank",
        UZUM_INFO
    )


@router.message(
    PaymentState.waiting_receipt,
    F.photo | F.document
)
async def receive_receipt(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    data = await state.get_data()

    method = data.get("payment_method")

    if message.photo:
        receipt_file_id = message.photo[-1].file_id
        receipt_type = "photo"

    elif message.document:
        receipt_file_id = message.document.file_id
        receipt_type = "document"

    else:
        await message.answer(
            "❌ Iltimos, chek rasmini yoki PDF faylini yuboring."
        )
        return

    payment_id = create_payment(
        user_id=message.from_user.id,
        payment_method=method,
        amount=PREMIUM_PRICE,
        receipt_file_id=receipt_file_id,
        receipt_type=receipt_type
    )

    await state.clear()

    await message.answer(
        "⏳ CHEKINGIZ QABUL QILINDI!\n\n"
        "To'lovingiz admin tomonidan tekshiriladi.\n"
        "Tasdiqlangandan keyin Premium avtomatik faollashadi."
    )

    user = message.from_user

    admin_text = (
        "💳 YANGI PREMIUM TO'LOV\n\n"
        f"🧾 To'lov ID: #{payment_id}\n"
        f"👤 Foydalanuvchi: {user.full_name}\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"🔗 Username: @{user.username or 'yoq'}\n\n"
        f"💳 To'lov usuli: {method}\n"
        f"💰 Summa: {PREMIUM_PRICE} so'm\n\n"
        "Pastdagi tugmalardan birini tanlang 👇"
    )

    if receipt_type == "photo":
        await bot.send_photo(
            ADMIN_ID,
            photo=receipt_file_id,
            caption=admin_text,
            reply_markup=admin_payment_keyboard(payment_id)
        )
    else:
        await bot.send_document(
            ADMIN_ID,
            document=receipt_file_id,
            caption=admin_text,
            reply_markup=admin_payment_keyboard(payment_id)
        )


@router.message(PaymentState.waiting_receipt)
async def receipt_wrong_type(message: Message):
    await message.answer(
        "❌ Chekni rasm yoki PDF ko'rinishida yuboring."
    )
