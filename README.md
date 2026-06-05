# 🏛 Ulfatlar Choyxonasi — Telegram Bot

🚀 **Ulfatlar Choyxonasi** is a fully automated Telegram bot tailored for restaurants and teahouses. Built on a modern asynchronous backend architecture, it provides a seamless dual-language (Latin/Cyrillic) interface for browsing menus, managing a real-time shopping cart, and booking tables.

---

## ✨ Features

* **🌐 True Dual-Language Interface:** Users can experience the bot completely in either Uzbek Latin (`uz_lat`) or Uzbek Cyrillic (`uz_cyr`). The system saves and remembers each user's language preference across sessions.
* **🍽 Dynamic Inline Menu:** Categories and products are rendered dynamically using inline keyboards, showcasing appetizing names, prices, descriptions, and high-quality food images.
* **🛒 Smart Shopping Cart:** Interactive asynchronous cart modifications allow users to increment, decrement `[➕] / [➖]`, or remove items instantly. Total prices update dynamically without sending repetitive messages.
* **📅 Table Booking Wizard (FSM):** A step-by-step Finite State Machine guide collects the reservation date/time, guest count, customer name, and phone number (via a native contact request button).
* **🔔 Live Admin Notifications:** Confirmed reservations and orders are instantly pushed to the restaurant's internal private Telegram group/channel for real-time tracking.
* **📞 Restaurant Info Hub:** Provides operational hours, official contact channels, and automated direct redirection links to Google Maps.

---

## 🛠 Tech Stack

* **Language:** Python 3.13+
* **Framework:** [Aiogram 3.x](https://github.com/aiogram/aiogram) (Advanced Asynchronous Telegram Bot Framework)
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async engine configuration)
* **Database:** PostgreSQL / SQLite
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (Blazing fast Python package installer and resolver)

---

## 📂 Project Structure

```text
UlfatlarChoyxonasi/
├── config/
│   ├── config.py          # API Tokens, Group IDs, and system configurations
│   └── strings.py         # Complete dictionary for Latin and Cyrillic strings
├── database/
│   ├── base.py            # Async DB engine setup and SessionLocal factories
│   ├── models.py          # SQLAlchemy schemas (User, Category, Product, Cart)
│   └── requests.py        # Optimized asynchronous database query routines
├── handlers/
│   ├── common.py          # /start command, language toggle, and general info
│   ├── menu.py            # Menu parsing, category clicks, and product rendering
│   ├── cart.py            # Real-time cart calculation and item modifiers
│   └── booking.py         # Table reservation pipeline handled via FSM
├── keyboards/
│   ├── reply.py           # Dynamic main reply keyboards matching user language
│   └── inline.py          # Interactive inline callback structures
├── states/
│   └── checkout.py        # FSM schema declarations for booking and ordering
├── utils/
│   └── callback_data.py   # Strongly-typed factory prefixes (CartAction, Clicks)
├── main.py                # Bot bootstrapping and polling activation point
└── README.md              # Documentation

⚙️ Local Development Setup
1. Clone the Repository
Bash

git clone [https://github.com/yourusername/UlfatlarChoyxonasi.git](https://github.com/yourusername/UlfatlarChoyxonasi.git)
cd UlfatlarChoyxonasi

2. Configure Environment Variables

Open config/config.py and input your respective credentials:
Python

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_GROUP_ID = -100xxxxxxxxx  # Target group ID for notification payloads

3. Spin up the Bot Using uv

Since the project leverages the lightning-fast uv workflow manager, virtual environment instantiation and dependency tracking happen completely out of the box with a single command:
Bash

uv run main.py

🚀 24/7 Production Deployment

To keep the bot up and running permanently on a cloud VPS instance (Ubuntu/Debian) even after terminating your terminal session, encapsulate it within a native systemd supervisor wrapper:

    Create a service manifest unit file:

Bash

sudo nano /etc/systemd/system/ulfatlarbot.service

    Paste the following declarative unit block (ensure your absolute paths map out correctly):

Ini, TOML

[Unit]
Description=Ulfatlar Choyxonasi Telegram Bot Daemon
After=network.target

[Service]
User=root
WorkingDirectory=/root/UlfatlarChoyxonasi
ExecStart=/root/.local/bin/uv run main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

    Reload system control, cache execution units, activate, and start the daemon:

Bash

sudo systemctl daemon-reload
sudo systemctl enable ulfatlarbot.service
sudo systemctl start ulfatlarbot.service

    Verify live production runtime telemetry logs:

Bash

sudo systemctl status ulfatlarbot.service

👨‍💻 Author

    Asilbek — Backend Developer — https://github.com/asilbekusmonov-gh