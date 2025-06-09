from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import os

TOKEN = os.environ.get("BOT_TOKEN")

WELCOME_MESSAGE = (
    "مرحبًا بك في محامي.كوم ⚖️\n"
    "نحن هنا لمساعدتك في الحصول على استشارات قانونية موثوقة تساعدك على فهم حقوقك واتخاذ قراراتك بثقة.\n\n"
    "✅ لا نطلب أي معلومات شخصية\n"
    "🗑️ يتم حذف المحادثة تلقائيًا من السيرفرات فور انتهائها — خصوصيتك أولويتنا\n\n"
    "📋 اختر أحد الخيارات من القائمة أدناه للبدء:"
)

ABOUT_MESSAGE = (
    "عن محامي.كوم ⚖️\n\n"
    "\"محامي.كوم\" هو أول منصة عراقية ذكية متخصصة في تقديم استشارات قانونية مبسّطة وآمنة تساعدك على فهم حقوقك والتعامل مع القضايا القانونية بثقة.\n\n"
    "نحن نؤمن أن الوصول إلى المعرفة القانونية حق للجميع، لذلك نوفر لك معلومات دقيقة ومبسطة دون الحاجة للكشف عن أي بيانات شخصية.\n\n"
    "🔒 الخصوصية أولويتنا:\n"
    "لا نطلب معلومات شخصية، ويتم حذف المحادثة تلقائيًا بعد انتهائها من خوادمنا.\n\n"
    "💡 لماذا محامي.كوم؟\n"
    "👥 أول منصة قانونية عراقية يديرها نخبة من المحامين والحقوقيين العراقيين\n"
    "✅ إجابات سريعة وواضحة\n"
    "🕔 متاحة في أي وقت\n"
    "📚 تغطي مختلف التخصصات القانونية (العقود، الأسرة، العمل، العقارات...)\n\n"
    "ابدأ الآن، واطمئن بأن استفسارك بين أيدٍ أمينة.\n\n"
    "لأي دعم أو ملاحظات: mohamycom@proton.me\n"
    "_(الخدمات الأساسية مجانية بالكامل)_"
)

MAIN_MENU = [
    ["استشارات قانونية (تلقائية)", "خدماتنا المدفوعة"],
    ["تعرف على حقوقك (مجاني)", "تصفح القوانين العراقية"],
    ["عن (محامي.كوم)"]
]

BACK_TO_MENU = [[KeyboardButton("العودة إلى القائمة الرئيسية")]]

# إعداد متغيرات الخدمات المدفوعة
PAID_SERVICE, SERVICE_TYPE, WAITING_QUESTION = range(3)

SERVICE_OPTIONS = [
    [
        "تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)",
        "تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)",
        "تنظيم العقود الخاصة (100,000 د.ع)",
        "استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)"
    ],
    ["العودة إلى القائمة الرئيسية"]
]

SERVICE_PRICES = {
    "تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)": 50000,
    "تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)": 50000,
    "تنظيم العقود الخاصة (100,000 د.ع)": 100000,
    "استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)": None
}

LAWYER_USER_ID = 8109994800
LAWYER_USERNAME = "mohamycom"
LAWYER_EMAIL = "mohamycom@proton.me"
LAWYER_WHATSAPP = "07775535047"

user_questions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
    elif text == "عن (محامي.كوم)":
        reply_markup = ReplyKeyboardMarkup(BACK_TO_MENU, resize_keyboard=True)
        await update.message.reply_text(ABOUT_MESSAGE, reply_markup=reply_markup)
    elif text == "خدماتنا المدفوعة":
        reply_markup = ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True)
        await update.message.reply_text(
            "🟢 الخدمة المدفوعة - استشارة خاصة\n\n"
            "- هذه الخدمة مخصصة للاستشارات القانونية الحساسة التي تحتاج إلى إجابة من مختصين ذوي خبرة.\n\n"
            "اختر من القائمة أدناه نوع الخدمة بالتحديد:",
            reply_markup=reply_markup
        )
        return SERVICE_TYPE
    elif text in sum(MAIN_MENU, []):  # باقي الأزرار
        reply_markup = ReplyKeyboardMarkup(BACK_TO_MENU, resize_keyboard=True)
        await update.message.reply_text("سيتم تفعيل الخدمة قريبا", reply_markup=reply_markup)

async def service_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in SERVICE_PRICES:
        context.user_data["selected_service_type"] = text
        service_price = SERVICE_PRICES.get(text)
        if service_price is not None:
            price_msg = f"- تكلفة الاستشارة: {service_price:,} دينار عراقي."
        else:
            price_msg = "- تكلفة الاستشارة: سيتم تحديدها بعد مراجعة المحامي."
        reply_markup = ReplyKeyboardMarkup([["نعم، أوافق"], ["إلغاء"]], resize_keyboard=True)
        await update.message.reply_text(
            f"🟢 الخدمة المدفوعة - {text}\n\n"
            "- هذه الخدمة مخصصة للاستشارات القانونية الحساسة التي تحتاج إلى إجابة من مختصين ذوي خبرة.\n"
            f"{price_msg}\n"
            "هل توافق على الشروط وتريد متابعة طلب الاستشارة؟",
            reply_markup=reply_markup
        )
        return PAID_SERVICE
    elif text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text("يرجى اختيار نوع خدمة من القائمة.")

async def paid_service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "نعم، أوافق":
        await update.message.reply_text(
            "يرجى كتابة استفسارك بشكل مفصل ليتم تحويله للمحامي المختص."
        )
        return WAITING_QUESTION
    else:
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("تم إلغاء الطلب.", reply_markup=reply_markup)
        return ConversationHandler.END

async def question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    question = update.message.text
    chat_id = update.message.chat_id
    service_type = context.user_data.get("selected_service_type", "غير محدد")
    service_price = SERVICE_PRICES.get(service_type)

    question_id = len(user_questions) + 1
    user_questions[question_id] = {
        "user_id": chat_id,
        "question": question,
        "service_type": service_type,
        "service_price": service_price
    }

    msg = (
        f"استفسار مدفوع جديد\n"
        f"رقم الاستفسار: {question_id}\n"
        f"نوع الخدمة: {service_type}\n"
        f"من: {user.full_name} (@{user.username or 'بدون يوزرنيم'})\n"
        f"نص الاستفسار:\n{question}\n\n"
        f"للرد بالموافقة أرسل:\n/accept{question_id}"
    )
    await update.message.reply_text(
        "تم إرسال استفسارك للمحامي المختص.\n"
        "سيتم إعلامك عند الموافقة على طلبك."
    )
    await context.bot.send_message(chat_id=LAWYER_USER_ID, text=msg)
    return ConversationHandler.END

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"حدث خطأ: {context.error}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
        states={
            SERVICE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_type_handler)],
            PAID_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, paid_service_handler)],
            WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_handler)],
        },
        fallbacks=[MessageHandler(filters.Regex("^العودة إلى القائمة الرئيسية$"), menu_handler)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()