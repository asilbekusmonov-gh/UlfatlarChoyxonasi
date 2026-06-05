import re
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from states.checkout import BookTableStates
from config.config import ADMIN_GROUP_ID
from database.requests import get_user_language
from keyboards.reply import get_main_menu

booking_router = Router()

BOOK_BUTTONS = ["📅 Joy band qilish", "📅 Жой банд қилиш"]


# 1. Bron qilishni boshlash
@booking_router.message(F.text.in_(BOOK_BUTTONS), StateFilter("*"))
async def start_booking(message: Message, state: FSMContext):
    await state.clear()
    lang = await get_user_language(message.from_user.id)
    await state.update_data(user_lang=lang)  # Tilni FSM ichida ham saqlab turamiz

    text = (
        "📅 <b>Joy band qilish (Bron):</b>\n\n"
        "Iltimos, kelmoqchi bo'lgan <b>sana va vaqtingizni</b> yozing.\n"
        "<i>Masalan: 8-iyun, soat 18:00 da</i>" if lang == "uz_lat" else
        "📅 <b>Жой банд қилиш (Брон):</b>\n\n"
        "Илтимос, келмоқчи бўлган <b>сана ва вақтингизни</b> ёзинг.\n"
        "<i>Масалан: 8-июн, соат 18:00 да</i>"
    )
    await message.answer(text, parse_mode="HTML")
    await state.set_state(BookTableStates.waiting_for_datetime)


# 2. Kelish vaqtini qabul qilish
@booking_router.message(BookTableStates.waiting_for_datetime)
async def process_booking_datetime(message: Message, state: FSMContext):
    await state.update_data(book_datetime=message.text)
    data = await state.get_data()
    lang = data['user_lang']

    text = (
        "👥 <b>Mehmonlar soni:</b>\n\nNecha kishi uchun joy band qilmoqchisiz?\n<i>Masalan: 6 kishi</i>" if lang == "uz_lat" else
        "👥 <b>Меҳмонлар сони:</b>\n\nНеча киши учун жой банд қилмоқчисиз?\n<i>Масалан: 6 киши</i>"
    )
    await message.answer(text, parse_mode="HTML")
    await state.set_state(BookTableStates.waiting_for_guests)


# 3. Mehmonlar sonini qabul qilish
@booking_router.message(BookTableStates.waiting_for_guests)
async def process_booking_guests(message: Message, state: FSMContext):
    await state.update_data(book_guests=message.text)
    data = await state.get_data()
    lang = data['user_lang']

    text = "👤 <b>Ismingizni kiriting:</b>" if lang == "uz_lat" else "👤 <b>Исмингизни киритинг:</b>"
    await message.answer(text, parse_mode="HTML")
    await state.set_state(BookTableStates.waiting_for_name)


# 4. Ismni qabul qilish va telefon so'rash
@booking_router.message(BookTableStates.waiting_for_name)
async def process_booking_name(message: Message, state: FSMContext):
    await state.update_data(book_name=message.text)
    data = await state.get_data()
    lang = data['user_lang']

    btn_text = "📱 Raqamni yuborish" if lang == "uz_lat" else "📱 Рақамни юбориш"
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn_text, request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )

    text = (
        "📱 <b>Telefon raqamingizni kiriting:</b>\n\n(Yoki pastdagi tugmani bosib yuboring)" if lang == "uz_lat" else
        "📱 <b>Телефон рақамингизни киритинг:</b>\n\n(Ёки пастдаги тугмани босиб юборинг)"
    )
    await message.answer(text, reply_markup=phone_keyboard, parse_mode="HTML")
    await state.set_state(BookTableStates.waiting_for_phone)


# 5. Telefon raqamni tekshirish va yakunlash
@booking_router.message(BookTableStates.waiting_for_phone)
async def process_booking_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['user_lang']
    phone_number = None

    if message.contact:
        phone_number = message.contact.phone_number
    elif message.text:
        clean_phone = re.sub(r"[\s\-\(\)\+]", "", message.text)
        if re.match(r"^(998)?\d{9}$", clean_phone):
            phone_number = "+" + (clean_phone if clean_phone.startswith("998") else "998" + clean_phone)
        else:
            error_text = (
                "⚠️ <b>Noto'g'ri format!</b>\nRaqamni kiriting (Masalan: +998931234567) yoki tugmani bosing:" if lang == "uz_lat" else
                "⚠️ <b>Нотўғри формат!</b>\nРақамни киритинг (Масалан: +998931234567) ёки тугмани босинг:"
            )
            await message.answer(error_text, parse_mode="HTML")
            return

    if phone_number:
        success_text = (
            "🎉 <b>Joyingiz muvaffaqiyatli band qilindi!</b>\n\nRestoran administratorimiz tez orada siz bilan bog'lanib, bronni tasdiqlaydi." if lang == "uz_lat" else
            "🎉 <b>Жойингиз муваффақиятли банд қилинди!</b>\n\nРесторан администраторимиз тез орада сиз билан боғланиб, бронни тасдиқлайди."
        )
        await message.answer(success_text, reply_markup=get_main_menu(lang), parse_mode="HTML")

        # Admirlarga har doim tushunarli tilda (masalan lotinchada) boradi
        admin_text = (
            f"📅 <b>YANGI STOL BRON QILINDI!</b>\n\n"
            f"👤 <b>Mijoz:</b> {data['book_name']}\n"
            f"📞 <b>Telefon:</b> {phone_number}\n"
            f"⏰ <b>Vaqt:</b> {data['book_datetime']}\n"
            f"👥 <b>Mehmonlar:</b> {data['book_guests']}\n"
            f"🔗 <b>Profil:</b> @{message.from_user.username if message.from_user.username else 'Mavjud emas'}"
        )
        await message.bot.send_message(chat_id=ADMIN_GROUP_ID, text=admin_text, parse_mode="HTML")
        await state.clear()