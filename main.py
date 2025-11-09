
import os
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask

# === CONFIG ===
BOT_TOKEN = "7614410181:AAGQ9J89lUXhQAuIWdBDPtBX5RT_teGPbFY"      # paste your real bot token here (keep it private)
CHANNEL_ID = -1003277266634  # paste your real channel ID here

# === FLASK APP (keeps Render web service alive) ===
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# === TELEGRAM BOT ===
async def copy_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and not message.text.startswith('/'):  # ignores commands like /start
        await context.bot.copy_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, copy_message))
    app.run_polling()

# === START BOTH THREADS ===
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()