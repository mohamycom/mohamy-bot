from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = (
    "(محامي.كوم) هو بوت متخصص في تقديم الاستشارات القانونية التي تساعدك على فهم حقوقك\n"
    "لانحتاج الى اي معلومات شخصية وسيتم حذف المحادثة تلقائيا من السيرفرات فور انتهاء المحادثة\n"
    "اختر من القائمة ادناه"
)

MAIN_MENU = [
    ["استشارات قانونية (تلقائية)"],
    ["خدماتنا المدفوعة"],
    ["تعرف على حقوقك (مجاني)"],
    ["تصفح القوانين العراقية"],
    ["عن (محامي.كوم)"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"لقد قلت: {update.message.text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == '__main__':
    main()