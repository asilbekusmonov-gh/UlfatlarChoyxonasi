import os
from pathlib import Path
from dotenv import load_dotenv

# Loyihaning asosiy (ildiz) papkasini avtomatik hisoblash
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylidan muhit o'zgaruvchilarini yuklash
load_dotenv(dotenv_path=BASE_DIR / ".env")

# ==========================================
# 1. Maxfiy Kalitlar (O'qish va Tekshirish)
# ==========================================
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Iltimos, .env faylini tekshiring.")

# Telegram ID-lar raqam bo'lgani uchun uni integer (int) turiga o'giramiz
ADMIN_GROUP_ID: int = int(os.getenv("ADMIN_GROUP_ID", 0))


# ==========================================
# 2. Restoran Statik Sozlamalari
# ==========================================
CURRENCY = "UZS"
ITEMS_PER_PAGE = 6  # Kelajakda menyu kattalashsa, sahifalarga bo'lish (pagination) uchun


RESTAURANT_INFO = {
    "name": "Ulfatlar Choyxonasi",
    "description": "Haqiqiy milliy taomlar lezzati, birodarlar uchrashadigan maskan! Premium masalliqlardan tayyorlangan maxsus oosh va quyuq sho'rvalarimizdan bahramand bo'ling.",
    "address": "📍 Toshkent sh., Amir Temur shoh ko'chasi, 42-uy",
    "working_hours": "🕒 Har kuni: 11:00 dan 23:00 gacha"
}


CONTACT_INFO = {
    "phone": "📞 +998 (71) 123-45-67",
    "telegram": "✈️ @ulfatlar_admin",
    "additional": "💬 Tadbirlar va marosimlar uchun buyurtmalarni kamida 24 soat oldin xabar qilishingizni so'raymiz."
}