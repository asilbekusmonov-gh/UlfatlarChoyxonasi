import asyncio
from database.base import init_db, async_session_maker
from database.models import Category, Product


async def seed_data():
    # Ma'lumotlar bazasi jadvallari mavjudligini ta'minlash
    await init_db()

    async with async_session_maker() as session:
        # 1. Kategoriyalarni qo'shish
        palov = Category(name="Palovlar")
        shorva = Category(name="Sho'rvalar")
        salads = Category(name="Salatlar")
        drinks = Category(name="Ichimliklar")

        session.add_all([palov, shorva, salads, drinks])
        await session.flush()  # ID-larni avtomatik generatsiya qilish uchun bazaga yuborish

        # 2. Mahsulotlarni (Taomlarni) qo'shish
        p1 = Product(
            category_id=palov.id,
            name="To'y Osh",
            description="Premium lazer guruchidan, sarxil go'sht va mayizlar bilan damlangan haqiqiy Toshkent to'y oshi.",
            price=120000.0,
            unit="kg"
        )
        p2 = Product(
            category_id=shorva.id,
            name="Go'shtli Sho'rva",
            description="Past olovda uzoq qaynatilgan, mayin pishgan go'sht va kartoshkali quyuq milliy sho'rva.",

            price=50000.0,
            unit="porsiya"
        )
        p3 = Product(
            category_id=salads.id,
            name="Achchiq-chuchuk",
            description="Yangi uzilgan shirin pomidor, piyoz va ko'katlardan tayyorlangan an'anaviy palovoldi salati.",
            price=15000.0,
            unit="porsiya"
        )
        p4 = Product(
            category_id=drinks.id,
            name="Fanta 1L",
            description="Muzdek va tetiklashtiruvchi gazli apelsin ta'mli ichimlik.",
            price=15000.0,
            unit="idish"
        )

        session.add_all([p1, p2, p3, p4])
        await session.commit()

    print("Ma'lumotlar bazasi Ulfatlar Choyxonasi taomlari bilan muvaffaqiyatli to'ldirildi!")


if __name__ == "__main__":
    asyncio.run(seed_data())