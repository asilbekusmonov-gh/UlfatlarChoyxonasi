# keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config.strings import STRINGS


def get_language_keyboard() -> ReplyKeyboardMarkup:
    """Tilni tanlash tugmalari (Botga birinchi marta kirganda chiqadi)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbekcha (Lotin)"), KeyboardButton(text="🇺🇿 Ўзбекча (Крилл)")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    """Foydalanuvchi tiliga moslashtirilgan asosiy menyu"""
    s = STRINGS[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=s["menu_btn"]),
                KeyboardButton(text=s["cart_btn"])
            ],
            [
                KeyboardButton(text=s["book_btn"])
            ],
            [
                KeyboardButton(text=s["about_btn"]),
                KeyboardButton(text=s["contact_btn"])
            ],
            [
                KeyboardButton(text=s["lang_btn"])  # Tilni o'zgartirish tugmasi
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyudan biror bo'limni tanlang..." if lang == "uz_lat" else "Менюдан бирор бўлимни танланг..."
    )


def get_phone_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Foydalanuvchi tiliga moslangan telefon raqamini yuborish tugmasi"""
    text = "📱 Telefon raqamni yuborish" if lang == "uz_lat" else "📱 Телефон рақамни юбориш"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Foydalanuvchi tiliga moslangan lokatsiyani yuborish tugmasi"""
    text = "📍 Manzilni (Lokatsiyani) yuborish" if lang == "uz_lat" else "📍 Манзилни (Локацияни) юбориш"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text, request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )