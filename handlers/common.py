from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import RESTAURANT_INFO, CONTACT_INFO
# config/strings.py faylidagi STRINGS lug'atini va baza so'rovlarini import qilamiz
from config.strings import STRINGS
from database.requests import set_user_language, get_user_language
from keyboards.reply import get_language_keyboard, get_main_menu

common_router = Router()


@common_router.message(CommandStart(), StateFilter("*"))
async def cmd_start(message: Message, state: FSMContext):
    """/start bosilganda tilni tanlashni so'rash"""
    await state.clear()
    await message.answer(
        "Xush kelibsiz! / Хуш келибсиз!\n"
        "Iltimos, tilni tanlang: / Илтимос, тилни танланг:",
        reply_markup=get_language_keyboard()
    )


@common_router.message(F.text == "🇺🇿 O'zbekcha (Lotin)", StateFilter("*"))
async def set_lang_latin(message: Message, state: FSMContext):
    """Lotin alifbosi tanlanganda"""
    await state.clear()
    # session argumentini olib tashladik, funksiyaning o'zi sessiyani hal qiladi
    await set_user_language(message.from_user.id, "uz_lat")

    welcome_text = STRINGS["uz_lat"]["welcome"].format(name=message.from_user.full_name)
    await message.answer(welcome_text, reply_markup=get_main_menu("uz_lat"))


@common_router.message(F.text == "🇺🇿 Ўзбекча (Крилл)", StateFilter("*"))
async def set_lang_cyrillic(message: Message, state: FSMContext):
    """Krill alifbosi tanlanganda"""
    await state.clear()
    await set_user_language(message.from_user.id, "uz_cyr")

    welcome_text = STRINGS["uz_cyr"]["welcome"].format(name=message.from_user.full_name)
    await message.answer(welcome_text, reply_markup=get_main_menu("uz_cyr"))


LANG_BUTTONS = ["🌐 Tilni o'zgartirish", "🌐 Тилни ўзгартириш"]

@common_router.message(F.text.in_(LANG_BUTTONS), StateFilter("*"))
async def change_language(message: Message, state: FSMContext):
    """Mijoz xohlagan paytda asosiy menyudan turib tilni qayta o'zgartira olishi uchun"""
    await state.clear()  # Eski holatlarni tozalaydi
    await message.answer(
        "Tilni tanlang / Тилни танланг:",
        reply_markup=get_language_keyboard()
    )


@common_router.message(F.text.in_(["ℹ️ Restoran haqida", "ℹ️ Ресторан ҳақида"]), StateFilter("*"))
async def show_about(message: Message):
    """Restoran haqida ma'lumot"""
    lang = await get_user_language(message.from_user.id)

    if lang == "uz_lat":
        about_text = (
            f"🏛 <b>{RESTAURANT_INFO['name']}</b>\n\n"
            f"{RESTAURANT_INFO['description']}\n\n"
            f"📍 <b>Manzil:</b> {RESTAURANT_INFO['address']}\n"
            f"⏰ <b>Ish vaqti:</b> {RESTAURANT_INFO['working_hours']}\n\n"
            f"🌐 <a href='http://maps.google.com/maps?q=41.3323,69.2828'>Google Xaritada ko'rish</a>"
        )
    else:
        about_text = (
            f"🏛 <b>{RESTAURANT_INFO['name']}</b>\n\n"
            f"{RESTAURANT_INFO['description_cyr'] if 'description_cyr' in RESTAURANT_INFO else RESTAURANT_INFO['description']}\n\n"
            f"📍 <b>Манзил:</b> {RESTAURANT_INFO['address_cyr'] if 'address_cyr' in RESTAURANT_INFO else RESTAURANT_INFO['address']}\n"
            f"⏰ <b>Иш вақти:</b> {RESTAURANT_INFO['working_hours_cyr'] if 'working_hours_cyr' in RESTAURANT_INFO else RESTAURANT_INFO['working_hours']}\n\n"
            f"🌐 <a href='http://maps.google.com/maps?q=41.3323,69.2828'>Google Харитада кўриш</a>"
        )

    await message.answer(about_text, parse_mode="HTML", disable_web_page_preview=False)


@common_router.message(F.text.in_(["📞 Kontaktlar", "📞 Контактлар"]), StateFilter("*"))
async def show_contact(message: Message, state: FSMContext):
    """Kontaktlar bo'limi"""
    await state.clear()
    lang = await get_user_language(message.from_user.id)

    if lang == "uz_lat":
        contact_text = (
            f"📞 <b>Aloqa ma'lumotlari:</b>\n\n"
            f"Telefon: {CONTACT_INFO['phone']}\n"
            f"Telegram admin: {CONTACT_INFO['telegram']}\n\n"
            f"{CONTACT_INFO['additional']}"
        )
    else:
        contact_text = (
            f"📞 <b>Алоқа маълумотлари:</b>\n\n"
            f"Телефон: {CONTACT_INFO['phone']}\n"
            f"Телеграм админ: {CONTACT_INFO['telegram']}\n\n"
            f"{CONTACT_INFO['additional_cyr'] if 'additional_cyr' in CONTACT_INFO else CONTACT_INFO['additional']}"
        )

    await message.answer(contact_text, parse_mode="HTML")