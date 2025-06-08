from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = (
    "(محامي.كوم) هو بوت متخصص في تقديم الاستشارات القانونية التي تساعدك على فهم حقوقك\n"
    "لانحتاج الى اي معلومات شخصية وسيتم حذف المحادثة تلقائيا من السيرفرات فور انتهاء المحادثة\n"
    "اختر من القائمة ادناه"
)

# ترتيب الأزرار بشكل أفقي (اثنين في كل سطر)
MAIN_MENU = [
    ["استشارات قانونية (تلقائية)", "خدماتنا المدفوعة"],
    ["تعرف على حقوقك (مجاني)", "تصفح القوانين العراقية"],
    ["عن (محامي.كوم)"]
]

BACK_TO_MENU = [[KeyboardButton("العودة إلى القائمة الرئيسية")]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
    elif text in sum(MAIN_MENU, []):  # إذا ضغط المستخدم على أحد أزرار القائمة
        reply_markup = ReplyKeyboardMarkup(BACK_TO_MENU, resize_keyboard=True)
        await update.message.reply_text("سيتم تفعيل الخدمة قريبا", reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    app.run_polling()

if __name__ == '__main__':
    main()