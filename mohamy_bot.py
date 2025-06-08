import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ===== لوحات المفاتيح =====
def main_keyboard():
    return ReplyKeyboardMarkup([
        ["استشارة قانونية تلقائية", "خدماتنا المدفوعة"],
        ["تواصل مع مطوري البوت", "تعرف على حقوقك (مجاني)"],
        ["تصفح القوانين العراقية", "عن محامي . كوم"]
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

# ===== معالجة الأوامر =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """🔒 **مرحبًا بك في بوت محامي.كوم** ⚖️

نحن نحترم خصوصيتك تمامًا. لا حاجة لذكر أي معلومات شخصية أو بيانات حقيقية. 
كما أن الأسئلة لا تُخزن ولا يتم تتبع المستخدمين.

اختر من القائمة أدناه الخدمة التي تناسبك:"""
    await update.message.reply_text(
        welcome_msg,
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "استشارة قانونية تلقائية":
        await update.message.reply_text(
            "🧾 سعر الاستشارة التلقائية هو 5000 دينار عراقي.\nاختر نوع القضية:",
            reply_markup=legal_advice_keyboard()
        )

    elif text == "خدماتنا المدفوعة":
        await update.message.reply_text(
            "⚖️ **الخدمات المميزة المتاحة**:\n\n"
            "1. صياغة العقود:\n"
            "   - الحكومية: 100,000 د.ع\n"
            "   - الشخصية: 250,000 د.ع\n"
            "2. تنظيم قضايا (حسب نوع القضية)\n"
            "3. استشارة خاصة: 50,000 د.ع\n\n"
            "📌 *الأسعار قابلة للتغيير وسيتم إشعارك بذلك قبل بدء الاستشارة.*\n\n"
            "اختر الخدمة التي تريدها:",
            reply_markup=paid_services_keyboard(),
            parse_mode="Markdown"
        )

    elif text == "صياغة العقود الشخصية والحكومية":
        context.user_data.update({
            'service': "صياغة العقود",
            'price': 100000  # افتراضيًا للحكومية
        })
        await update.message.reply_text(
            "📝 **خدمة صياغة العقود**\n\n"
            "السعر:\nالحكومية: 100,000 د.ع\nالشخصية: 250,000 د.ع\n\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )

    elif text == "استشارة خاصة":
        context.user_data.update({
            'service': "استشارة خاصة",
            'price': 50000
        })
        await update.message.reply_text(
            "💼 **استشارة خاصة**\n\n"
            "السعر: 50,000 د.ع\nهل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )

    elif text == "نعم، اريد المتابعة للدفع":
        service = context.user_data.get('service', 'خدمة غير محددة')
        price = context.user_data.get('price', 0)
        payment_link = f"https://payment.mohamy.com/?service={service.replace(' ', '_')}&amount={price}"
        await update.message.reply_text(
            f"🔐 **تفاصيل الدفع**\n\n"
            f"الخدمة: {service}\n"
            f"المبلغ: {price} د.ع\n\n"
            f"للاستمرار، يرجى الدفع عبر الرابط الآمن:\n{payment_link}",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )

    elif text in ["لا، شكراً", "العودة للرئيسية"]:
        await update.message.reply_text(
            "تم العودة للقائمة الرئيسية",
            reply_markup=main_keyboard()
        )

    elif text == "تواصل مع مطوري البوت":
        await update.message.reply_text(
            "👨‍💻 للتواصل مع مطوري البوت:\n\n"
            "للمساهمة أو إرسال الملاحظات على البوت، لا تتردد في مراسلتنا على:\n"
            "واتساب: +9647775535047\n"
            "أوقات الرد: 6م - 10م"
        )

    elif text == "تعرف على حقوقك (مجاني)":
        await update.message.reply_text("📚 هذا القسم قيد التطوير. سيتم نشر معلومات قانونية مفيدة قريبًا.")

    elif text == "تصفح القوانين العراقية":
        await update.message.reply_text("📖 هذه الخدمة ستتيح لك قريبًا استعراض نصوص القوانين العراقية.")

    elif text == "عن محامي . كوم":
        await update.message.reply_text(
            "🤖 تم تأسيس بوت محامي.كوم بهدف تسهيل وصول الأفراد إلى المعلومات القانونية والخدمات الاستشارية بأسلوب عصري وسهل، وبعيدًا عن التعقيد التقليدي في المجال القانوني."
        )

async def main():
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # الحصول على التوكن من متغير البيئة
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN environment variable not set.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
