import json
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler, CallbackQueryHandler

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
    ["نصائح وارشادات قانونية", "عن (محامي.كوم)"]
]

BACK_TO_MENU = [[KeyboardButton("العودة إلى القائمة الرئيسية")]]
PAID_REPLY_MARKUP = ReplyKeyboardMarkup([["نعم، أوافق"], ["إلغاء"], ["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)
ONLY_BACK_MARKUP = ReplyKeyboardMarkup([["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)

PAID_SERVICE, SERVICE_TYPE, WAITING_QUESTION, WAITING_REJECTION_REASON = range(4)

SERVICE_OPTIONS = [
    [
        "قضايا موظفي الدولة في الوزارات كافة",
        "قضايا منتسبي الجيش العراقي (ضباطا ومراتب)"
    ],
    [
        "صياغة العقود الخاصة",
        "استفسارات قانونية اخرى"
    ],
    ["العودة إلى القائمة الرئيسية"]
]
SERVICE_PRICES = {
    "قضايا موظفي الدولة في الوزارات كافة": 50000,
    "قضايا منتسبي الجيش العراقي (ضباطا ومراتب)": 50000,
    "صياغة العقود الخاصة": 100000,
    "استفسارات قانونية اخرى": None
}
SERVICE_NAMES_DISPLAY = {
    "قضايا موظفي الدولة في الوزارات كافة": "قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)",
    "قضايا منتسبي الجيش العراقي (ضباطا ومراتب)": "قضايا منتسبي الجيش العراقي (ضباطا ومراتب) (50,000 د.ع)",
    "صياغة العقود الخاصة": "صياغة العقود الخاصة (100,000 د.ع)",
    "استفسارات قانونية اخرى": "استفسارات قانونية اخرى (السعر يُحدد بعد مراجعة المحامي)"
}

LAWYER_USER_ID = 8109994800
LAWYER_USERNAME = "mohamycom"
LAWYER_EMAIL = "mohamycom@proton.me"
LAWYER_WHATSAPP = "07775535047"
ACCOUNT_NUMBER = "9916153415"

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
    elif text in sum(MAIN_MENU, []):
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
        await update.message.reply_text("يرجى اختيار نوع خدمة من القائمة.", reply_markup=ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True))
        return SERVICE_TYPE

async def paid_service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "نعم، أوافق":
        await update.message.reply_text(
            "يرجى ملاحظة ما يلي:\n"
            "1. ان طريقة تحويل الاموال تتم في الوقت الحالي عبر تطبيق سوبر كي المدعوم من قبل مصرف الرافدين ولاتتوفر طريقة دفع اخرى .\n"
            "2. كتابة  الاستفسار كاملا برسالة واحدة وعدم اجتزاءه برسائل متعددة.\n"
            "3. ستتم مراجعة الاستفسار من قبل محامين متخصصين وفي حال الموافقة سيتم ارسال اشعار اليكم بذلك متضمنا كيفية الدفع .\n"
            "شكرا لتفهمكم",
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

    lawyer_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("موافقة", callback_data=f"approve_{question_id}"),
            InlineKeyboardButton("رفض", callback_data=f"reject_{question_id}")
        ]
    ])

    msg = (
        f"استفسار مدفوع جديد\n"
        f"رقم الاستفسار: {question_id}\n"
        f"نوع الخدمة: {service_display}\n"
        f"من: {user.full_name} (@{user.username or 'بدون يوزرنيم'})\n"
        f"نص الاستفسار:\n{question}\n\n"
        f"اختر الإجراء المناسب:"
    )
    await update.message.reply_text(
        "تم إرسال استفسارك للمحامي المختص.\n"
        "سيتم إعلامك عند الموافقة على طلبك.",
        reply_markup=ONLY_BACK_MARKUP
    )
    await context.bot.send_message(chat_id=LAWYER_USER_ID, text=msg, reply_markup=lawyer_markup)
    return ConversationHandler.END

async def lawyer_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("approve_"):
        question_id = int(data.replace("approve_", ""))
        load_questions()
        if question_id in user_questions:
            q = user_questions[question_id]
            user_id = q["user_id"]
            service_type = q["service_type"]
            service_price = q["service_price"]
            service_display = SERVICE_NAMES_DISPLAY.get(service_type, service_type)

            contact_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("التواصل عبر التليجرام", callback_data=f"contact_telegram_{question_id}")],
                [InlineKeyboardButton("التواصل عبر الواتساب", callback_data=f"contact_whatsapp_{question_id}")],
                [InlineKeyboardButton("التواصل عبر الايميل", callback_data=f"contact_email_{question_id}")]
            ])

            if service_price is not None:
                accept_message = (
                    "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                    f"نوع الخدمة: {service_display}\n"
                    f"تكلفة الخدمة: {service_price:,} دينار عراقي\n\n"
                    f"يرجى التحويل الى رقم الحساب الاتي  {ACCOUNT_NUMBER}\n\n"
                    "بعد التحويل يمكنك اختيار طريقة التواصل التي تناسبك بالضغط على الزر المناسب 👇"
                )
            else:
                accept_message = (
                    "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                    f"نوع الخدمة: {service_display}\n"
                    "تكلفة الخدمة: سيتم إعلامك بالسعر بعد مراجعة المحامي.\n\n"
                    f"يرجى التحويل الى رقم الحساب الاتي  {ACCOUNT_NUMBER}\n\n"
                    "بعد التحويل يمكنك اختيار طريقة التواصل التي تناسبك بالضغط على الزر المناسب 👇"
                )
            try:
                await context.bot.send_message(chat_id=user_id, text=accept_message, reply_markup=contact_markup)
            except Exception as e:
                await query.edit_message_text(f"حدث خطأ أثناء محاولة إرسال رسالة القبول للمستخدم: {e}")
                return
            await query.edit_message_text("تم إعلام المستخدم بالموافقة.")
            del user_questions[question_id]
            save_questions()
        else:
            await query.edit_message_text("لم يتم العثور على هذا الاستفسار.")
    elif data.startswith("reject_"):
        question_id = int(data.replace("reject_", ""))
        context.user_data["rejected_question_id"] = question_id
        await query.edit_message_text("يرجى كتابة سبب رفض الاستفسار (سيُرسل للمستخدم):")
        return WAITING_REJECTION_REASON
    elif data.startswith("contact_"):
        parts = data.split("_")
        method = parts[1]
        if method == "telegram":
            text = f"معلومات التواصل عبر التليجرام:\n@{LAWYER_USERNAME}"
        elif method == "whatsapp":
            text = f"معلومات التواصل عبر الواتساب:\n{LAWYER_WHATSAPP}"
        elif method == "email":
            text = f"معلومات التواصل عبر البريد الإلكتروني:\n{LAWYER_EMAIL}"
        else:
            text = "طريقة التواصل غير معروفة."
        await query.answer()
        await query.message.reply_text(text)

async def rejection_reason_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text
    question_id = context.user_data.get("rejected_question_id")
    load_questions()
    if question_id and question_id in user_questions:
        q = user_questions[question_id]
        user_id = q["user_id"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"❌ تم رفض استفسارك من قبل المحامي.\n\nسبب الرفض: {reason}",
            reply_markup=ONLY_BACK_MARKUP
        )
        del user_questions[question_id]
        save_questions()
        await update.message.reply_text("تم إرسال سبب الرفض للمستخدم وحذف الاستفسار.", reply_markup=ONLY_BACK_MARKUP)
    else:
        await update.message.reply_text("لم يتم العثور على هذا الاستفسار.", reply_markup=ONLY_BACK_MARKUP)
    return ConversationHandler.END

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"حدث خطأ: {context.error}")

def main():
    load_questions()
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)
        ],
        states={
            SERVICE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_type_handler)],
            PAID_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, paid_service_handler)],
            WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_handler)],
            WAITING_REJECTION_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, rejection_reason_handler)],
        },
        fallbacks=[MessageHandler(filters.Regex("^العودة إلى القائمة الرئيسية$"), menu_handler)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(lawyer_callback_handler))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()