from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.requests import get_all_categories, get_products_by_category, get_product_by_id, get_user_language
from keyboards.inline import get_categories_keyboard, get_products_keyboard, get_product_detail_keyboard
from utils.callback_data import CategoryClick, ProductClick
from config.strings import STRINGS  # Faqat STRINGS ning o'zi qoldi

menu_router = Router()

# Ikkala tildagi tugma matnlarini shu yerning o'zida ro'yxatga olib qo'yamiz
MENU_BUTTONS = ["🍽 Menyuni ko'rish", "🍽 Менюни кўриш"]


@menu_router.message(F.text.in_(MENU_BUTTONS))  # Endi bu xatosiz ishlaydi
@menu_router.message(Command("menu"))
async def show_menu(message: Message):
    """Mijoz 'Menyuni ko'rish' tugmansini bosganda yoki /menu yuborganda"""
    categories = await get_all_categories()

    # Foydalanuvchi tilini bazadan olamiz
    lang = await get_user_language(message.from_user.id)

    if not categories:
        empty_text = "Hozircha menyu bo'sh. Tez orada taomlar qo'shiladi!" if lang == "uz_lat" else "Ҳозирча меню бўш. Тез орада таомлар қўшилиши кутилмоқда!"
        await message.answer(empty_text)
        return

    # Matnni foydalanuvchi tiliga qarab dinamik chiqaramiz
    select_text = STRINGS[lang]["select_section"]
    await message.answer(select_text, reply_markup=get_categories_keyboard(categories))


@menu_router.callback_query(CategoryClick.filter())
async def process_category_click(callback: CallbackQuery, callback_data: CategoryClick):
    """Kategoriya tugmasi bosilganda undagi taomlarni ko'rsatish"""
    products = await get_products_by_category(callback_data.id)
    lang = await get_user_language(callback.from_user.id)

    if not products:
        alert_text = "Bu bo'limda hozircha taomlar mavjud emas." if lang == "uz_lat" else "Бу бўлимда ҳозирча таомлар мавжуд эмас."
        await callback.answer(alert_text, show_alert=True)
        return

    title_text = "🍲 Taomni tanlang:" if lang == "uz_lat" else "🍲 Таомни танланг:"
    await callback.message.edit_text(title_text, reply_markup=get_products_keyboard(products))
    await callback.answer()


@menu_router.callback_query(ProductClick.filter())
async def process_product_click(callback: CallbackQuery, callback_data: ProductClick):
    """Bitta taom bosilganda uning rasmi, narxi va ta'rifini chiqarish"""
    product = await get_product_by_id(callback_data.id)
    lang = await get_user_language(callback.from_user.id)

    if not product:
        alert_text = "Mahsulot topilmadi." if lang == "uz_lat" else "Маҳсулот топилмади."
        await callback.answer(alert_text, show_alert=True)
        return

    # Matnni tilga moslab shakllantiramiz
    if lang == "uz_lat":
        caption_text = (
            f"🔸 **{product.name}**\n\n"
            f"📝 Ta'rifi: {product.description}\n\n"
            f"💵 Narxi: {product.price:,} UZS ({product.unit})"
        )
    else:
        caption_text = (
            f"🔸 **{product.name}**\n\n"
            f"📝 Таърифи: {product.description}\n\n"
            f"💵 Нархи: {product.price:,} UZS ({product.unit})"
        )

    # 1. Oldingi matnli menyu xabarini o'chirib tashlaymiz (chunki matnli xabarga rasm yopishtirib bo'lmaydi)
    await callback.message.delete()

    # 2. Rasm bor yoki yo'qligini tekshirib, yangi rasmli xabar yuboramiz
    if product.image:
        # Agar bazada rasm (file_id yoki URL) bo'lsa, rasmli xabar yuboramiz
        await callback.message.answer_photo(
            photo=product.image,
            caption=caption_text,
            parse_mode="Markdown",
            reply_markup=get_product_detail_keyboard(product.id)
        )
    else:
        # Agar mabodo rasm yuklanmagan bo'lsa, bot sinib qolmasligi uchun faqat matn yuboradi
        await callback.message.answer(
            text=caption_text,
            parse_mode="Markdown",
            reply_markup=get_product_detail_keyboard(product.id)
        )

    await callback.answer()


@menu_router.callback_query(F.data == "back_to_categories")
async def back_to_categories_handler(callback: CallbackQuery):
    """Taomlar ro'yxatidan yoki taom ichidan ortga (kategoriyalarga) qaytish"""
    categories = await get_all_categories()
    lang = await get_user_language(callback.from_user.id)

    if not categories:
        alert_text = "Kategoriyalar topilmadi." if lang == "uz_lat" else "Категориялар топилмади."
        await callback.answer(alert_text, show_alert=True)
        return

    select_text = STRINGS[lang]["select_section"]
    await callback.message.edit_text(
        text=select_text,
        reply_markup=get_categories_keyboard(categories)
    )
    await callback.answer()


@menu_router.callback_query(F.data == "close_menu")
async def close_menu_handler(callback: CallbackQuery):
    """Kategoriyalar menyusida '❌ Menyuni yopish' tugmasi bosilganda xabarni o'chirish"""
    lang = await get_user_language(callback.from_user.id)
    try:
        await callback.message.delete()
    except Exception:
        close_text = "Menyu yopildi." if lang == "uz_lat" else "Меню ёпилди."
        await callback.message.edit_text(close_text)
    await callback.answer()