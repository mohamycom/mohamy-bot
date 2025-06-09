import json
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

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
PAID_REPLY_MARKUP = ReplyKeyboardMarkup([["نعم، أوافق"], ["إلغاء"], ["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)
ONLY_BACK_MARKUP = ReplyKeyboardMarkup([["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)

# إعداد متغيرات الخدمات المدفوعة
PAID_SERVICE, SERVICE_TYPE, WAITING_QUESTION = range(3)

# خيارات الخدمات المدفوعة (بدون ذكر المبلغ)
SERVICE_OPTIONS = [
    [
        "تنظيم قضايا موظفي الدولة في الوزارات كافة",
        "تنظيم قضايا منتسبي الجيش العراقي"
    ],
    [
        "تنظيم العقود الخاصة",
        "استفسارات قانونية أخرى"
    ],
    ["العودة إلى القائمة الرئيسية"]
]

SERVICE_PRICES = {
    "تنظيم قضايا موظفي الدولة في الوزارات كافة": 50000,
    "تنظيم قضايا منتسبي الجيش العراقي": 50000,
    "تنظيم العقود الخاصة": 100000,
    "استفسارات قانونية أخرى": None
}

SERVICE_NAMES_DISPLAY = {
    "تنظيم قضايا موظفي الدولة في الوزارات كافة": "تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)",
    "تنظيم قضايا منتسبي الجيش العراقي": "تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)",
    "تنظيم العقود الخاصة": "تنظيم العقود الخاصة (100,000 د.ع)",
    "استفسارات قانونية أخرى": "استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)"
}

LAWYER_USER_ID = 8109994800
LAWYER_USERNAME = "mohamycom"
LAWYER_EMAIL = "mohamycom@proton.me"
LAWYER_WHATSAPP = "07775535047"

QUESTIONS_FILE = "user_questions.json"
user_questions = {}

def save_questions():
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_questions, f, ensure_ascii=False)

def load_questions():
    global user_questions
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            user_questions = json.load(f)
            user_questions = {int(k): v for k, v in user_questions.items()}
    except Exception:
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
        service_display = SERVICE_NAMES_DISPLAY.get(text, text)
        if service_price is not None:
            price_msg = f"- تكلفة الاستشارة: {service_price:,} دينار عراقي."
        else:
            price_msg = "- تكلفة الاستشارة: سيتم تحديدها بعد مراجعة المحامي."
        await update.message.reply_text(
            f"🟢 الخدمة المدفوعة - {service_display}\n\n"
            "- هذه الخدمة مخصصة للاستشارات القانونية الحساسة التي تحتاج إلى إجابة من مختصين ذوي خبرة.\n"
            f"{price_msg}\n"
            "هل توافق على الشروط وتريد متابعة طلب الاستشارة؟",
            reply_markup=PAID_REPLY_MARKUP
        )
        return PAID_SERVICE
    elif text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text("يرجى اختيار نوع خدمة من القائمة.", reply_markup=PAID_REPLY_MARKUP)

async def paid_service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "نعم، أوافق":
        await update.message.reply_text(
            "يرجى كتابة استفسارك بشكل مفصل ليتم تحويله للمحامي المختص.",
            reply_markup=ONLY_BACK_MARKUP
        )
        return WAITING_QUESTION
    elif text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)
        return ConversationHandler.END
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
    service_display = SERVICE_NAMES_DISPLAY.get(service_type, service_type)

    load_questions()
    question_id = max(user_questions.keys(), default=0) + 1
    user_questions[question_id] = {
        "user_id": chat_id,
        "question": question,
        "service_type": service_type,
        "service_price": service_price
    }
    save_questions()

    msg = (
        f"استفسار مدفوع جديد\n"
        f"رقم الاستفسار: {question_id}\n"
        f"نوع الخدمة: {service_display}\n"
        f"من: {user.full_name} (@{user.username or 'بدون يوزرنيم'})\n"
        f"نص الاستفسار:\n{question}\n\n"
        f"للرد بالموافقة أرسل:\n/accept{question_id}"
    )
    await update.message.reply_text(
        "تم إرسال استفسارك للمحامي المختص.\n"
        "سيتم إعلامك عند الموافقة على طلبك.",
        reply_markup=ONLY_BACK_MARKUP
    )
    await context.bot.send_message(chat_id=LAWYER_USER_ID, text=msg)
    return ConversationHandler.END

async def accept_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith("/accept"):
        return
    try:
        question_id = int(text.replace("/accept", ""))
    except Exception:
        await update.message.reply_text("صيغة رقم الاستفسار غير صحيحة.")
        return

    load_questions()
    if question_id in user_questions:
        q = user_questions[question_id]
        user_id = q["user_id"]
        service_type = q["service_type"]
        service_price = q["service_price"]
        service_display = SERVICE_NAMES_DISPLAY.get(service_type, service_type)

        reply_markup = ONLY_BACK_MARKUP

        if service_price is not None:
            accept_message = (
                "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                f"نوع الخدمة: {service_display}\n"
                f"تكلفة الخدمة: {service_price:,} دينار عراقي\n\n"
                "يمكنك الآن إكمال إجراءات الدفع والتواصل عبر أحد الطرق التالية:\n\n"
                f"1️⃣ تيليجرام: @{LAWYER_USERNAME}\n"
                f"2️⃣ الإيميل: {LAWYER_EMAIL}\n"
                f"3️⃣ واتساب: {LAWYER_WHATSAPP}\n\n"
                "يرجى إرسال صورة التحويل أو رقم العملية عبر الوسيلة التي تفضلها، وسيتم الرد عليك بعد التأكد.\n\n"
                "يرجى عدم التواصل مع الطرق اعلاه الا عندما يتم تحويل المبلغ المحدد وسيتم اهمال اي رسالة قبل ذلك\n"
                "شكرا لتفهمكم"
            )
        else:
            accept_message = (
                "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                f"نوع الخدمة: {service_display}\n"
                "تكلفة الخدمة: سيتم إعلامك بالسعر بعد مراجعة المحامي.\n\n"
                "يمكنك الآن إكمال إجراءات الدفع والتواصل عبر أحد الطرق التالية:\n\n"
                f"1️⃣ تيليجرام: @{LAWYER_USERNAME}\n"
                f"2️⃣ الإيميل: {LAWYER_EMAIL}\n"
                f"3️⃣ واتساب: {LAWYER_WHATSAPP}\n\n"
                "يرجى إرسال صورة التحويل أو رقم العملية عبر الوسيلة التي تفضلها، وسيتم الرد عليك بعد التأكد.\n\n"
                "يرجى عدم التواصل مع الطرق اعلاه الا عندما يتم تحويل المبلغ المحدد وسيتم اهمال اي رسالة قبل ذلك\n"
                "شكرا لتفهمكم"
            )
        try:
            await context.bot.send_message(chat_id=user_id, text=accept_message, reply_markup=reply_markup)
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء محاولة إرسال رسالة القبول للمستخدم: {e}")
            return
        await update.message.reply_text("تم إعلام المستخدم بالموافقة.")
        del user_questions[question_id]
        save_questions()
    else:
        await update.message.reply_text("لم يتم العثور على هذا الاستفسار.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"حدث خطأ: {context.error}")

def main():
    load_questions()
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
    app.add_handler(MessageHandler(filters.Regex(r"^/accept\d+$"), accept_handler))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()