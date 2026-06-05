from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.requests import add_to_cart, get_user_cart, modify_cart_quantity, get_user_language
from keyboards.inline import get_cart_keyboard
from utils.callback_data import CartAction

cart_router = Router()

# Ikkala tildagi Savatcha tugmasi matnlari
CART_BUTTONS = ["🛒 Savatcha", "🛒 Саватча"]


@cart_router.callback_query(CartAction.filter(F.action == "add"))
async def process_add_to_cart(callback: CallbackQuery, callback_data: CartAction):
    """Taom sahifasida '📥 Savatchaga qo'shish' tugmasi bosilganda"""
    await add_to_cart(user_id=callback.from_user.id, product_id=callback_data.product_id)
    lang = await get_user_language(callback.from_user.id)

    alert_text = "✅ Mahsulot savatchaga qo'shildi!" if lang == "uz_lat" else "✅ Маҳсулот саватчага қўшилди!"
    await callback.answer(alert_text, show_alert=False)


@cart_router.message(F.text.in_(CART_BUTTONS))
async def show_cart(message: Message):
    """Mijoz pastki reply menyudan '🛒 Savatcha' tugmasini bosganda"""
    cart = await get_user_cart(message.from_user.id)
    lang = await get_user_language(message.from_user.id)

    # Agar savatcha ochilmagan bo'lsa yoki ichi bo'sh bo'lsa
    if not cart or not cart.items:
        empty_text = (
            "🛒 Savatchangiz hozircha bo'sh. Menyudan taomlarni tanlab qo'shishingiz mumkin." if lang == "uz_lat" else
            "🛒 Саватчангиз ҳозирча бўш. Менюдан таомларни танлаб қўшишингиз mumkin."
        )
        await message.answer(empty_text)
        return

    # Savatchadagi umumiy summani hisoblaymiz
    total_price = sum(item.product.price * item.quantity for item in cart.items)

    # Savatcha matnini shakllantiramiz
    if lang == "uz_lat":
        cart_text = "🛒 **Sizning savatchangiz:**\n\n"
        for idx, item in enumerate(cart.items, 1):
            item_total = item.product.price * item.quantity
            cart_text += f"{idx}. **{item.product.name}**\n   {item.quantity} {item.product.unit} x {item.product.price:,} = {item_total:,} UZS\n\n"
        cart_text += f"💵 **Umumiy summa:** {total_price:,} UZS"
    else:
        cart_text = "🛒 **Сизнинг саватчангиз:**\n\n"
        for idx, item in enumerate(cart.items, 1):
            item_total = item.product.price * item.quantity
            cart_text += f"{idx}. **{item.product.name}**\n   {item.quantity} {item.product.unit} x {item.product.price:,} = {item_total:,} UZS\n\n"
        cart_text += f"💵 **Умумий сумма:** {total_price:,} UZS"

    await message.answer(cart_text, parse_mode="Markdown", reply_markup=get_cart_keyboard(cart.items))


@cart_router.callback_query(CartAction.filter(F.action.in_({"incr", "decr", "remove"})))
async def process_cart_modifications(callback: CallbackQuery, callback_data: CartAction):
    """Savatcha ichida [➕], [➖] yoki [🗑 O'chirish] tugmalari bosilganda"""
    await modify_cart_quantity(
        user_id=callback.from_user.id,
        product_id=callback_data.product_id,
        action=callback_data.action
    )

    cart = await get_user_cart(callback.from_user.id)
    lang = await get_user_language(callback.from_user.id)

    # Agar oxirgi mahsulot ham o'chib ketgan bo'lsa
    if not cart or not cart.items:
        empty_text = "🛒 Savatchangiz bo'shab qoldi." if lang == "uz_lat" else "🛒 Саватчангиз бўшаб қолди."
        await callback.message.edit_text(empty_text)
        await callback.answer()
        return

    # Agar savatchada hali mahsulot bo'lsa, summani qayta hisoblaymiz
    total_price = sum(item.product.price * item.quantity for item in cart.items)

    if lang == "uz_lat":
        cart_text = "🛒 **Sizning savatchangiz:**\n\n"
        for idx, item in enumerate(cart.items, 1):
            item_total = item.product.price * item.quantity
            cart_text += f"{idx}. **{item.product.name}**\n   {item.quantity} {item.product.unit} x {item.product.price:,} = {item_total:,} UZS\n\n"
        cart_text += f"💵 **Umumiy summa:** {total_price:,} UZS"
    else:
        cart_text = "🛒 **Сизнинг саватчангиз:**\n\n"
        for idx, item in enumerate(cart.items, 1):
            item_total = item.product.price * item.quantity
            cart_text += f"{idx}. **{item.product.name}**\n   {item.quantity} {item.product.unit} x {item.product.price:,} = {item_total:,} UZS\n\n"
        cart_text += f"💵 **Умумий сумма:** {total_price:,} UZS"

    await callback.message.edit_text(cart_text, parse_mode="Markdown", reply_markup=get_cart_keyboard(cart.items))
    await callback.answer()


@cart_router.callback_query(F.data == "none")
async def process_none_callback(callback: CallbackQuery):
    """Savatchadagi mahsulot nomi yozilgan o'rtadagi tugma bosilganda hech narsa qilmaslik uchun"""
    await callback.answer()