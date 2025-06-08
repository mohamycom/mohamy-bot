from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os

TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = (
    "مرحبا بكم في مساعدكم (محامي.كوم) وهو بوت متخصص في تقديم الاستشارات القانونية الاحترافية التي تساعدك على فهم حقوقك واتخاذ القرار القانوني الصحيح بثقة.\n\n"
    "لا نحتاج الى اي معلومات شخصية (مثل الاسم او العنوان او رقم الهاتف ...إلخ) وسيتم حذف الاستشارات تلقائيا من السيرفرات فور انتهاء المحادثة فلا داعي للقلق حيال ذلك."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"لقد قلت: {update.message.text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == '__main__':
    main()