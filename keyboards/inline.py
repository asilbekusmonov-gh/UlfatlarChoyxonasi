from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.callback_data import CategoryClick, ProductClick, CartAction


def get_categories_keyboard(categories) -> InlineKeyboardMarkup:
    """Barcha kategoriyalarni inline tugma qilib chiqarish"""
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=cat.name, callback_data=CategoryClick(id=cat.id))
    builder.adjust(2)  # Kategoriyalarni 2 tadan qilib teradi

    # Yangi qator qo'shib, unga menyuni yopish tugmasini joylashtiramiz
    builder.row(
        InlineKeyboardButton(text="❌ Menyuni yopish", callback_data="close_menu")
    )
    return builder.as_markup()


def get_products_keyboard(products) -> InlineKeyboardMarkup:
    """Kategoriya ichidagi mahsulotlarni inline tugma qilib chiqarish"""
    builder = InlineKeyboardBuilder()
    for prod in products:
        builder.button(text=f"{prod.name} - {prod.price:,} UZS", callback_data=ProductClick(id=prod.id))
    builder.button(text="🔙 Orqaga", callback_data="back_to_categories")
    builder.adjust(1)  # Har bir taom alohida qatorda
    return builder.as_markup()


def get_product_detail_keyboard(product_id: int) -> InlineKeyboardMarkup:
    """Bitta taomning ichiga kirganda chiqadigan tugmalar"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📥 Savatchaga qo'shish", callback_data=CartAction(action="add", product_id=product_id))
    builder.button(text="🔙 Menyuga qaytish", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()


def get_cart_keyboard(cart_items) -> InlineKeyboardMarkup:
    """Savatcha ichidagi mahsulotlarni boshqarish tugmalari"""
    builder = InlineKeyboardBuilder()

    for item in cart_items:
        # Har bir mahsulot uchun 3 ta tugmadan iborat qator yaratamiz: [-] [Taom nomi (X ta)] [+]
        builder.row(
            InlineKeyboardButton(text="➖", callback_data=CartAction(action="decr", product_id=item.product_id).pack()),
            InlineKeyboardButton(text=f"{item.product.name} ({item.quantity} {item.product.unit})",
                                 callback_data="none"),
            InlineKeyboardButton(text="➕", callback_data=CartAction(action="incr", product_id=item.product_id).pack())
        )
        # Mahsulotni butunlay o'chirish tugmasi
        builder.row(
            InlineKeyboardButton(text=f"🗑 {item.product.name}ni o'chirish",
                                 callback_data=CartAction(action="remove", product_id=item.product_id).pack())
        )

    # Eng pastga buyurtma berish tugmasini qo'shamiz
    builder.row(
        InlineKeyboardButton(text="🚖 Buyurtma berish", callback_data="checkout")
    )
    return builder.as_markup()