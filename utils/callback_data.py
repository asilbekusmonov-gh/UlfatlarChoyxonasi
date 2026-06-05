from aiogram.filters.callback_data import CallbackData

class CategoryClick(CallbackData, prefix="cat"):
    id: int

class ProductClick(CallbackData, prefix="prod"):
    id: int

class CartAction(CallbackData, prefix="cart"):
    action: str  # "add" (qo'shish), "incr" (ko'paytirish), "decr" (kamaytirish), "remove" (o'chirish)
    product_id: int