import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand  # Buyruqlar menyusi uchun import
from config.config import BOT_TOKEN
from database.base import init_db
from handlers.booking import booking_router
from handlers.common import common_router
from handlers.menu import menu_router
from handlers.cart import cart_router
from handlers.checkout import checkout_router

logging.basicConfig(level=logging.INFO)


async def set_bot_commands(bot: Bot):
    """Botning chap burchagida turadigan buyruqlar menyusini sozlash"""
    commands = [
        BotCommand(command="start", description="Botni qayta ishga tushirish"),
        BotCommand(command="menu", description="Taomlar menyusini ko'rish"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # 1. SQLite ma'lumotlar bazasini ishga tushirish
    await init_db()
    logging.info("Ma'lumotlar bazasi muvaffaqiyatli sinxronizatsiya qilindi.")

    # 2. Bot va Dispatcher yorliqlarini sozlash
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Buyruqlar menyusini o'rnatamiz
    await set_bot_commands(bot)

    # Routerlarni dispatcherga ulaymiz
    dp.include_routers(
        common_router,
        menu_router,
        cart_router,
        checkout_router,
        booking_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot qo'lda to'xtatildi.")