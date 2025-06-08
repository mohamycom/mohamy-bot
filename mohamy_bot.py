import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد السجل لتتبع الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# رسالة الترحيب عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحبًا بك في بوت المحامي 👨‍⚖️\nأرسل سؤالك القانوني وسأقوم بالإجابة عليه.")

# التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # من الأفضل هنا توصيل الرسالة إلى نموذج ذكاء صناعي أو قاعدة بيانات، لكن سنرد برد ثابت كمثال
    reply = (
        "شكرًا لرسالتك.\n"
        "سيتم تحويل سؤالك القانوني إلى المحامي المختص والرد عليك في أقرب وقت ممكن.\n"
        "يرجى الانتظار..."
    )

    # إرسال الرد دون استخدام parse_mode لتجنب الخطأ
    await update.message.reply_text(reply)

# إنشاء التطبيق وتشغيل البوت
if __name__ == '__main__':
    import os
    TOKEN = os.getenv("BOT_TOKEN")  # تأكد أن المتغير هذا مضاف إلى بيئة Render

    if not TOKEN:
        raise ValueError("يرجى ضبط متغير البيئة BOT_TOKEN في Render")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 جاري تشغيل البوت...")
    app.run_polling()
