from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "ef main_keyboard():
    return ReplyKeyboardMarkup([
        ["استشارة قانونية تلقائية", "خدماتنا المدفوعة"],
        ["تواصل مع فريق المحامين", "تعرف على حقوقك"],
        ["عن محامي . كوم"]
    ], resize_keyboard=True)

def legal_advice_keyboard():
    return ReplyKeyboardMarkup([
        ["قضايا منتسبي الجيش", "قضايا موظفي الدولة"],
        ["قضايا جنائية", "العودة للرئيسية"]
    ], resize_keyboard=True)

def paid_services_keyboard():
    return ReplyKeyboardMarkup([
        ["صياغة العقود الشخصية والحكومية", "تنظيم قضايا"],
        ["استشارة خاصة", "العودة للرئيسية"]
    ], resize_keyboard=True)

# ========== معالجة الأوامر ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """💼 مرحبًا بك في بوت محامي.كوم ⚖️
نقدّم لك استشارات قانونية احترافية وخدمات مخصصة تساعدك على فهم حقوقك واتخاذ القرار القانوني الصحيح بثقة.

📌 اختر من القائمة أدناه الخدمة التي تناسب احتياجك:"""
    await update.message.reply_text(welcome_msg, reply_markup=main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "استشارة قانونية تلقائية":
        await update.message.reply_text(
            "اختر نوع القضية:",
            reply_markup=legal_advice_keyboard()
        )
    
    elif text == "خدماتنا المدفوعة":
        await update.message.reply_text(
            "الخدمات المميزة المتاحة:\n\n- صياغة العقود الشخصية والحكومية: \n- تنظيم قضايا: \n- استشارة خاصة: ",
            reply_markup=paid_services_keyboard()
        )
    
    elif text == "تواصل مع فريق المحامين":
        await update.message.reply_text(
            "📞 للتواصل المباشر:\n"
            "واتساب: +9647775535047\n"
            "ايميل: +++\n\n"
            "ساعات العمل للاستشارات الخاصة: 6م-10م (توقيت بغداد)"
        )
    
    elif text == "تعرف على حقوقك":
        await update.message.reply_text(
            "📚 اعرف حقوقك:\n"
            "1. حقوق الموظف في العراق\n"
            "2. حقوق المنتسب في الجيش وقوى الامن الداخلي\n"
            "3. اخرى\n\n"
            "اكتب الموضوع الذي تبحث عنه:"
        )
    
    elif text == "عن محامي . كوم":
        await update.message.reply_text(
            "⚖️ محامي.كوم - أول منصة قانونية عراقية ذكية\n\n"
            "تأسست عام 2025 لتقديم:\n"
            "- استشارات قانونية فورية\n"
            "- خدمات قانونية مميزة\n"
            "- نشر الوعي القانوني\n\n"
            "فريقنا: اكثر من 13 محامياً معتمداً"
        )
    
    elif text == "العودة للرئيسية":
        await update.message.reply_text(
            "تم العودة للقائمة الرئيسية",
            reply_markup=main_keyboard()
        )

# ========== إعداد البوت ==========
def main():
    print("جاري تشغيل بوت محامي.كوم...")
    
    try:
        application = Application.builder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("البوت يعمل الآن! اذهب إلى Telegram وابدأ المحادثة مع البوت")
        application.run_polling()
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
