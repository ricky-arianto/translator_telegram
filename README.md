# Telegram Translator Bot 🤖🌐

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Telegram](https://img.shields.io/badge/telegram-bot-blue?logo=telegram)
![OpenAI](https://img.shields.io/badge/OpenAI-API-red)

Telegram Translator Bot adalah bot Telegram yang dapat **menerjemahkan pesan secara otomatis** ke berbagai bahasa. Bot ini memanfaatkan **OpenAI API** untuk menghasilkan terjemahan yang natural dan akurat.

---

## 🎯 Fitur

- Terjemahkan pesan ke bahasa pilihan pengguna  
- Mendukung berbagai bahasa (English, Melayu, Jepang, dsb.)  
- Inline keyboard untuk memilih bahasa terjemahan  
- Mudah di-deploy di server lokal atau cloud  

---

## ⚙️ Teknologi

- **Python 3.x**  
- **python-telegram-bot** → komunikasi dengan Telegram  
- **OpenAI API** → proses penerjemahan AI  
- **python-dotenv** → load token & API key dari file `.env`  

---
## 🖼️ Preview Video
### Berikut adalah demo singkat cara kerja bot ini:

[![Telegram Translator Bot Demo](https://img.youtube.com/vi/S8mZalYZ3eY/0.jpg)](https://youtube.com/shorts/S8mZalYZ3eY?feature=share)

## 💾 Instalasi

1. Clone repositori:

```bash
git clone https://github.com/username/telegram-translator-bot.git
cd telegram-translator-bot
Install dependensi:

bash
Copy code
pip install -r requirements.txt
Buat file .env untuk token dan API key:

env
Copy code
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
Jalankan bot:

bash
Copy code
python bot.py

📂 Struktur Folder
text
Copy code
telegram-translator-bot/
├── bot.py            # File utama bot
├── requirements.txt  # Library Python
├── README.md         # Dokumentasi
└── .env              # File environment (tidak di-push ke GitHub)
🤝 Kontribusi
Kontribusi welcome!
Fork repositori → buat perubahan → pull request

📜 Lisensi
MIT License © 2025 Ricky Arianto

---
