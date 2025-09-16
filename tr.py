import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from openai import OpenAI

# ===== Load environment variables =====
load_dotenv()  # membaca file .env

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan! Pastikan ada di file .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY tidak ditemukan! Pastikan ada di file .env")

# Set environment variable untuk OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ===== Logging =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== OpenAI client =====
client = OpenAI()  # otomatis pakai OPENAI_API_KEY dari env

# ===== User storage =====
messages_original = {}   # message_id -> teks asli pengirim
messages_en = {}         # message_id -> teks English
user_language = {}       # user_id -> default bahasa (ISO code)

# ===== Start command =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    await update.message.reply_text(
        "Bot penerjemah siap! Ketik pesan apa saja. "
        "Gunakan /setlang untuk mengatur bahasa defaultmu. "
        "Tombol 'Translate to your language' akan menggunakan bahasa default yang sudah kamu set."
    )

# ===== Set language command =====
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user_id = update.message.from_user.id

    keyboard = [
        [InlineKeyboardButton(f"{flag} {name}", callback_data=f"setlang_{code}_{user_id}")]
        for code, name, flag in [
            ("id", "Indonesia", "🇮🇩"),
            ("ms", "Malay", "🇲🇾"),
            ("es", "Español", "🇪🇸"),
            ("fr", "Français", "🇫🇷"),
            ("jp", "日本語", "🇯🇵"),
            ("en", "English", "🇬🇧")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Pilih bahasa defaultmu:", reply_markup=reply_markup)

# ===== Callback handler =====
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is None:
        return
    query = update.callback_query
    await query.answer()

    data = query.data

    # ===== Set default language =====
    if data.startswith("setlang_"):
        parts = data.split("_")
        lang_code = parts[1]
        user_id = int(parts[2])
        user_language[user_id] = lang_code
        await query.edit_message_text(f"Bahasa defaultmu disimpan: {lang_code.upper()}")
        return

    # ===== Translate button =====
    if data.startswith("translate_"):
        msg_id = int(data.split("_")[1])
        user_id_click = query.from_user.id

        target_lang = user_language.get(user_id_click, query.from_user.language_code or "en")
        original_text = messages_original.get(msg_id)

        if not original_text:
            await query.answer("Pesan asli tidak ditemukan.", show_alert=True)
            return

        try:
            prompt = f"Terjemahkan teks berikut ke bahasa '{target_lang}' dengan akurat, tapi buat bahasanya terdengar alami dan santai, tidak terlalu baku atau formal. Pertahankan makna asli, termasuk nuansa atau gaya percakapan jika ada\n\n{original_text}"
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            translated_text = resp.choices[0].message.content

            # Kirim ke private chat user
            try:
                await context.bot.send_message(
                    chat_id=user_id_click,
                    text=f"**Terjemahan ({target_lang}):**\n{translated_text}",
                    parse_mode="Markdown"
                )
                await query.answer("Terjemahan dikirim ke chat pribadi Anda.", show_alert=True)
            except:
                await query.answer(
                    "Tidak bisa mengirim ke chat pribadi. Silakan /start chat dengan bot dulu.",
                    show_alert=True
                )

        except Exception as e:
            logger.error(f"Error translating: {e}")
            await query.answer("Terjadi error saat menerjemahkan.", show_alert=True)

# ===== Handle incoming messages =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return
    text = update.message.text

    try:
        # Translate ke English
        prompt = f"Terjemahkan teks berikut ke bahasa Inggris seakurat mungkin:\n\n{text}"
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        en_text = resp.choices[0].message.content

        msg = await update.message.reply_text(f"**English:**\n{en_text}", parse_mode="Markdown")
        messages_en[msg.message_id] = en_text
        messages_original[msg.message_id] = text

        # Tombol translate
        keyboard = [
            [InlineKeyboardButton("Translate to your language (private)", callback_data=f"translate_{msg.message_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_reply_markup(reply_markup)

    except Exception as e:
        logger.error(f"Error translating: {e}")
        await update.message.reply_text("Terjadi error saat menerjemahkan pesan.")

# ===== Main =====
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlang", set_language))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Translator bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
