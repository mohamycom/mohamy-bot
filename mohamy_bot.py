import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ========== إعدادات أساسية ==========
TOKEN = os.environ.get('TOKEN')  # التوكن من متغيرات البيئة في Render

# ========== لوحات المفاتيح ==========
def main_keyboard():
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

def payment_confirmation_keyboard():
    return ReplyKeyboardMarkup([
        ["نعم، اريد المتابعة للدفع", "لا، شكراً"]
    ], resize_keyboard=True)

# ========== معالجة الأوامر ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """🔒 **مرحبًا بك في بوت محامي.كوم - المنصة القانونية الآمنة** ⚖️

نقدّم لك استشارات قانونية احترافية مع ضمانات كاملة لخصوصيتك:

✅ **لا نحتاج أي معلومات شخصية** (اسم، عنوان، هوية)
✅ **لا يتم حفظ أي من محادثاتك** في سيرفراتنا
✅ **أسئلتك تختفي تلقائيًا** بعد انتهاء الجلسة
✅ **نظام تشفير متقدم** لحماية بياناتك

📌 اختر من القائمة أدناه الخدمة التي تناسب احتياجك:"""
    
    await update.message.reply_text(
        welcome_msg, 
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "استشارة قانونية تلقائية":
        await update.message.reply_text(
            "اختر نوع القضية:",
            reply_markup=legal_advice_keyboard()
        )
    
    elif text == "خدماتنا المدفوعة":
        await update.message.reply_text(
            "الخدمات المميزة المتاحة:\n\n"
            "1. صياغة العقود الشخصية والحكومية\n"
            "2. تنظيم قضايا\n"
            "3. استشارة خاصة\n\n"
            "اختر الخدمة التي تريدها:",
            reply_markup=paid_services_keyboard()
        )
    
    elif text == "صياغة العقود الشخصية والحكومية":
        context.user_data['selected_service'] = "صياغة العقود الشخصية والحكومية"
        context.user_data['service_price'] = 150
        
        await update.message.reply_text(
            "📝 **خدمة صياغة العقود الشخصية والحكومية**\n\n"
            "تشمل هذه الخدمة:\n"
            "- صياغة العقود وفقاً للقوانين العراقية\n"
            "- مراجعة العقود القائمة\n"
            "- تقديم نصائح قانونية لحماية حقوقك\n\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "تنظيم قضايا":
        context.user_data['selected_service'] = "تنظيم قضايا"
        context.user_data['service_price'] = 500
        
        await update.message.reply_text(
            "⚖️ **خدمة تنظيم قضايا**\n\n"
            "تشمل هذه الخدمة:\n"
            "- دراسة الموقف القانوني\n"
            "- إعداد المذكرات واللوائح\n"
            "- متابعة الإجراءات القضائية\n\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "استشارة خاصة":
        context.user_data['selected_service'] = "استشارة خاصة"
        context.user_data['service_price'] = 200
        
        await update.message.reply_text(
            "👨⚖️ **استشارة خاصة**\n\n"
            "تشمل هذه الخدمة:\n"
            "- جلسة استشارية خاصة مع محامي متخصص\n"
            "- تحليل قانوني مفصل لقضيتك\n"
            "- تقديم خيارات قانونية عملية\n\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "نعم، اريد المتابعة للدفع":
        service = context.user_data.get('selected_service', '')
        price = context.user_data.get('service_price', 0)
        
        if service and price > 0:
            payment_link = create_payment_link(service, price)
            await update.message.reply_text(
                f"🔐 **تفاصيل الدفع**\n\n"
                f"الخدمة: {service}\n"
                f"المبلغ: {price} ريال\n\n"
                f"للاستمرار، يرجى الدفع عبر الرابط الآمن:\n{payment_link}\n\n"
                "بعد اتمام الدفع، سيتم التواصل معك خلال 24 ساعة لاستكمال طلبك.",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                "حدث خطأ، يرجى اختيار الخدمة مرة أخرى",
                reply_markup=main_keyboard()
            )
    
    elif text in ["لا، شكراً", "العودة للرئيسية"]:
        await update.message.reply_text(
            "تم العودة للقائمة الرئيسية",
            reply_markup=main_keyboard()
        )
    
    elif text == "تواصل مع فريق المحامين":
        await update.message.reply_text(
            "📞 للتواصل المباشر:\n"
            "واتساب: +9647775535047\n"
            "ايميل: contact@mohamy.com\n\n"
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

def create_payment_link(service_name, amount):
    """إنشاء رابط دفع تجريبي (يمكن استبداله برابط حقيقي)"""
    return f"https://payment.mohamy.com/?service={service_name.replace(' ', '_')}&amount={amount}"

async def post_init(application: Application):
    """وظيفة لتنظيف أي Webhook قديم عند التشغيل"""
    await application.bot.delete_webhook()
    print("✅ تم تنظيف Webhook القديم")

def main():
    print("🚀 جاري تشغيل بوت محامي.كوم...")
    
    try:
        # إعداد البوت مع تأكيد تنظيف Webhook
        application = (
            Application.builder()
            .token(TOKEN)
            .post_init(post_init)
            .build()
        )
        
        # إضافة المعالجين
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ البوت يعمل في وضع Polling!")
        print("⏳ جاري الاستماع للرسائل...")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()