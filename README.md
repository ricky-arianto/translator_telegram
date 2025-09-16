#Telegram Translator Bot 🤖🌐






Telegram Translator Bot adalah bot Telegram yang dapat menerjemahkan pesan secara otomatis ke berbagai bahasa. Bot ini memanfaatkan OpenAI API untuk menghasilkan terjemahan yang natural dan akurat.

##🎯 Fitur

Terjemahkan pesan ke bahasa pilihan pengguna

Mendukung berbagai bahasa (English, Melayu, Jepang, dsb.)

Inline keyboard untuk memilih bahasa terjemahan

Mudah di-deploy di server lokal atau cloud

##⚙️ Teknologi

Python 3.x

python-telegram-bot → komunikasi dengan Telegram

OpenAI API → proses penerjemahan AI

python-dotenv → load token & API key dari file .env

##💾 Instalasi

Clone repositori:

git clone https://github.com/username/telegram-translator-bot.git
cd telegram-translator-bot


##Install dependensi:

pip install -r requirements.txt


Buat file .env untuk token dan API key:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key


##Jalankan bot:

python bot.py

🖼️ Preview Video

Berikut adalah demo singkat cara kerja bot ini:
https://youtube.com/shorts/S8mZalYZ3eY?feature=share

##📂 Struktur Folder
telegram-translator-bot/
│
├─ bot.py             # File utama bot
├─ requirements.txt   # Library Python
├─ README.md          # Dokumentasi
└─ .env               # File environment (tidak di-push ke GitHub)

##🤝 Kontribusi

Kontribusi welcome!
Fork repositori → buat perubahan → pull request

##📜 Lisensi

MIT License © 2025 Ricky Arianto
