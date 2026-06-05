from aiogram.fsm.state import StatesGroup, State

class CheckoutStates(StatesGroup):
    """Buyurtma rasmiylashtirish bosqichlari"""
    waiting_for_name = State()      # Ismini kiritishini kutish holati
    waiting_for_phone = State()     # Telefon raqamini kutish holati
    waiting_for_location = State()  # Lokatsiyasini kutish holati



class BookTableStates(StatesGroup):
    waiting_for_datetime = State()  # Sana va vaqtni kutish
    waiting_for_guests = State()    # Mehmonlar sonini kutish
    waiting_for_name = State()      # Ismni kutish
    waiting_for_phone = State()