from aiogram.fsm.state import State, StatesGroup


# ==========================================
# TO'LOV STATE'LARI
# ==========================================

class PaymentState(StatesGroup):
    waiting_receipt = State()


# ==========================================
# ADMIN PANEL STATE'LARI
# ==========================================

class AdminCourseState(StatesGroup):

    # --------------------------------------
    # BO'LIM QO'SHISH
    # --------------------------------------
    waiting_section_course = State()
    waiting_section_title = State()

    # --------------------------------------
    # VIDEO DARS QO'SHISH
    # --------------------------------------
    waiting_lesson_section = State()
    waiting_lesson_title = State()
    waiting_lesson_video = State()
    waiting_lesson_description = State()

    # --------------------------------------
    # PREMIUMNI QO'LDA BERISH
    # --------------------------------------
    waiting_manual_premium_user = State()

    # --------------------------------------
    # PREMIUMNI OLIB TASHLASH
    # --------------------------------------
    waiting_remove_premium_user = State()

    # --------------------------------------
    # VIDEO DARSI NOMI / TAVSIFINI TAHRIRLASH
    # --------------------------------------
    waiting_edit_lesson_title = State()
    waiting_edit_lesson_description = State()
    waiting_edit_lesson_video = State()

    # --------------------------------------
    # HAMMAGA XABAR YUBORISH
    # --------------------------------------
    waiting_broadcast_message = State()
