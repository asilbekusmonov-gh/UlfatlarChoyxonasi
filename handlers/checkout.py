from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from config.config import ADMIN_GROUP_ID
from database.requests import get_user_cart, clear_cart
from states.checkout import CheckoutStates
from keyboards.reply import get_phone_keyboard, get_location_keyboard, get_main_menu

checkout_router = Router()


@checkout_router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    """Savatchadagi '🚖 Buyurtma berish' tugmasi bosilganda"""
    cart = await get_user_cart(callback.from_user.id)
    if not cart or not cart.items:
        await callback.answer("Savatchangiz bo'sh!", show_alert=True)
        return

    # Birinchi bosqich: Ismni so'rash va holatni o'zgartirish
    await callback.message.answer(
        "🚖 Buyurtma berish jarayonini boshlaymiz.\n"
        "Iltimos, ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()  # Eski reply tugmalarni yashiramiz
    )
    await state.set_state(CheckoutStates.waiting_for_name)
    await callback.answer()


@checkout_router.message(CheckoutStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Mijoz ismini kiritganda"""
    await state.update_data(name=message.text)  # Ismni xotiraga saqlaymiz

    # Ikkinchi bosqich: Telefon raqamni maxsus tugma orqali so'rash
    await message.answer(
        "📱 Telefon raqamingizni kiriting:\n\n"
        "(Yoki pastdagi 'Raqamni yuborish' tugmasini bosing)",
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(CheckoutStates.waiting_for_phone)


import re  # Telefon raqamini tekshirish uchun Regular Expression (Regex) import qilamiz


# ... (boshqa importlar o'zgarishsiz qoladi)

@checkout_router.message(CheckoutStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Mijoz telefon raqamini tugma orqali yuborganda yoki qo'lda yozganda"""

    phone_number = None

    # 1. Agar mijoz maxsus tugmani bosib, kontaktini yuborgan bo'lsa
    if message.contact:
        phone_number = message.contact.phone_number

    # 2. Agar mijoz raqamni qo'lda yozib yuborgan bo'lsa
    elif message.text:
        # Raqam ichidagi bo'shliqlar (probel), chiziqchalar va qavslarni tozalaymiz
        clean_phone = re.sub(r"[\s\-\(\)\+]", "", message.text)

        # O'zbekiston raqamlari formatini tekshiramiz (998XXXXXXXXX yoki shunchaki 9 qatlamli raqam)
        # Masalan: 998931215477 yoki 931215477 formatlarini tekshirish
        if re.match(r"^(998)?\d{9}$", clean_phone):
            # Agar 998 siz yozgan bo'lsa, oldiga qo'shib qo'yamiz
            if not clean_phone.startswith("998"):
                phone_number = "+" + "998" + clean_phone
            else:
                phone_number = "+" + clean_phone
        else:
            # Agar kiritilgan matn telefon raqamiga o'xshamasa, qaytadan so'raymiz
            await message.answer(
                "⚠️ <b>Noto'g'ri format!</b>\n\n"
                "Iltimos, telefon raqamingizni qo'lda kiriting (Masalan: <code>+998931234567</code>) "
                "yoki pastdagi tugmani bosing.",
                parse_mode="HTML"
            )
            return

    # Agar raqam muvaffaqiyatli aniqlangan bo'lsa, saqlaymiz va keyingi bosqichga o'tamiz
    if phone_number:
        await state.update_data(phone=phone_number)

        # Keyingi bosqich: Lokatsiyani so'rash
        await message.answer(
            "📍 Oxirgi bosqich! Taomni qayerga yetkazib berish kerak? "
            "Pastdagi tugmani bosib joylashuvingizni (lokatsiya) yuboring yoki manzilni matn ko'rinishida yozing:",
            reply_markup=get_location_keyboard()
        )
        await state.set_state(CheckoutStates.waiting_for_location)


@checkout_router.message(CheckoutStates.waiting_for_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Mijoz lokatsiyasini yuborganda - Jarayon tugashi va adminga yuborish"""
    user_data = await state.get_data()
    cart = await get_user_cart(message.from_user.id)

    # Savatchadagi ma'lumotlarni tekst holatiga keltirish va summani hisoblash
    total_price = sum(item.product.price * item.quantity for item in cart.items)
    items_text = ""
    for idx, item in enumerate(cart.items, 1):
        item_total = item.product.price * item.quantity
        items_text += f"   {idx}. {item.product.name} — {item.quantity} {item.product.unit} x {item.product.price:,} = {item_total:,} UZS\n"

    # 1. Mijozga muvaffaqiyatli xabarini yuborish
    await message.answer(
        "🎉 Rahmat! Buyurtmangiz qabul qilindi va operatorimiz tez orada siz bilan bog'lanadi.",
        reply_markup=get_main_menu()  # Bosh menyuni qaytaramiz
    )

    # 2. Adminlar guruhiga buyurtma haqida to'liq hisobotni yuborish
    admin_text = (
        f"🔔 **YANGI BUYURTMA!**\n\n"
        f"👤 **Mijoz:** {user_data['name']}\n"
        f"📞 **Telefon:** {user_data['phone']}\n"
        f"🔗 **Profil:** @{message.from_user.username if message.from_user.username else 'Mavjud emas'}\n\n"
        f"🍲 **Taomlar:**\n{items_text}\n"
        f"💵 **Umumiy summa:** {total_price:,} UZS"
    )

    # Guruhga matnni yuboramiz
    admin_msg = await message.bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=admin_text,
        parse_mode="Markdown"
    )

    # Guruhga mijozning aniq lokatsiyasini ham yuboramiz (kuryer topib borishi uchun)
    await message.bot.send_location(
        chat_id=ADMIN_GROUP_ID,
        latitude=message.location.latitude,
        longitude=message.location.longitude,
        reply_to_message_id=admin_msg.message_id  # Asosiy xabarga javob (reply) ko'rinishida
    )

    # 3. Savatchani tozalash va holatni yakunlash (FSM xotirasini bo'shatish)
    await clear_cart(message.from_user.id)
    await state.clear()
