import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ.get('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! البوت يعمل الآن بنجاح ✅",
        reply_markup=ReplyKeyboardMarkup([["اختبار"]], resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"تم استلام: {update.message.text}")

async def main():
    print("🚀 جاري تشغيل البوت...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    await app.bot.delete_webhook()
    print("✅ البوت يعمل الآن!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())