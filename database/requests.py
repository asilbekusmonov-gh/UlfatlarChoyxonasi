from sqlalchemy import select, delete
from database.base import async_session_maker
from database.models import Category, Product, Cart, CartItem, Order, OrderItem
from database.base import async_session_maker

# ==========================================
# 1. Menu Operations
# ==========================================

async def get_all_categories() -> list[Category]:
    """Fetches all food categories for the main interactive menu."""
    async with async_session_maker() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()


async def get_products_by_category(category_id: int) -> list[Product]:
    """Fetches all items matching a chosen category partition."""
    async with async_session_maker() as session:
        result = await session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        return result.scalars().all()


async def get_product_by_id(product_id: int) -> Product | None:
    """Retrieves detailed info for a single product entry."""
    async with async_session_maker() as session:
        return await session.get(Product, product_id)


# ==========================================
# 2. Stateful Cart Operations
# ==========================================

async def add_to_cart(user_id: int, product_id: int):
    """Adds an item to the user's cart or increments quantity if it exists."""
    async with async_session_maker() as session:
        # Check if user has an existing cart parent record
        cart_stmt = await session.execute(select(Cart).where(Cart.user_id == user_id))
        cart = cart_stmt.scalar_one_or_none()

        if not cart:
            cart = Cart(user_id=user_id)
            session.add(cart)
            await session.flush()  # Generates cart.id without committing transaction

        # Check if product is already inside this specific cart
        item_stmt = await session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        item = item_stmt.scalar_one_or_none()

        if item:
            item.quantity += 1
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
            session.add(item)

        await session.commit()


async def modify_cart_quantity(user_id: int, product_id: int, action: str):
    """Handles real-time item increments, decrements, and total deletions from inline keys."""
    async with async_session_maker() as session:
        cart_stmt = await session.execute(select(Cart).where(Cart.user_id == user_id))
        cart = cart_stmt.scalar_one_or_none()
        if not cart:
            return

        item_stmt = await session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        item = item_stmt.scalar_one_or_none()
        if not item:
            return

        if action == "incr":
            item.quantity += 1
        elif action == "decr":
            if item.quantity > 1:
                item.quantity -= 1
            else:
                await session.delete(item)
        elif action == "remove":
            await session.delete(item)

        await session.commit()


async def get_user_cart(user_id: int) -> Cart | None:
    async with async_session_maker() as session:
        stmt = await session.execute(select(Cart).where(Cart.user_id == user_id))
        return stmt.scalar_one_or_none()


async def clear_cart(user_id: int):
    async with async_session_maker() as session:
        cart_stmt = await session.execute(select(Cart).where(Cart.user_id == user_id))
        cart = cart_stmt.scalar_one_or_none()
        if cart:
            await session.execute(delete(CartItem).where(CartItem.cart_id == cart.id))
            await session.commit()


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# O'zingizning model importlaringiz orasiga User ni ham qo'shing
from database.models import User


async def set_user_language(user_id: int, lang: str):
    """Foydalanuvchi tilini bazaga saqlash yoki yangilash"""
    async with async_session_maker() as session:  # Bu yerda import qilingan o'zgaruvchi chaqiriladi
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            user.language = lang
        else:
            user = User(id=user_id, language=lang)
            session.add(user)

        await session.commit()


async def get_user_language(user_id: int) -> str:
    """Foydalanuvchi tilini bazadan aniqlash (topilmasa lotin alifbosi default)"""
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return user.language if user else "uz_lat"