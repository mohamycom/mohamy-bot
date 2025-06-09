from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import os

TOKEN = os.environ.get("BOT_TOKEN")

LAWYER_USER_ID = 8109994800
LAWYER_USERNAME = "mohamycom"
LAWYER_EMAIL = "mohamycom@proton.me"
LAWYER_WHATSAPP = "07775535047"

PAID_SERVICE, SERVICE_TYPE, WAITING_QUESTION = range(3)

MAIN_MENU = [
    ["استشارات قانونية (تلقائية)", "خدماتنا المدفوعة"],
    ["تعرف على حقوقك (مجاني)", "تصفح القوانين العراقية"],
    ["عن (محامي.كوم)"]
]

SERVICE_OPTIONS = [
    ["تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)"],
    ["تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)"],
    ["تنظيم العقود الخاصة (100,000 د.ع)"],
    ["استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)"],
    ["العودة إلى القائمة الرئيسية"]
]

BACK_TO_MENU = [[KeyboardButton("العودة إلى القائمة الرئيسية")]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(
        "مرحبًا بك في محامي.كوم ⚖️\n"
        "اختر الخدمة التي تحتاجها من القائمة:",
        reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "خدماتنا المدفوعة":
        reply_markup = ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True)
        await update.message.reply_text(
            "يرجى اختيار نوع الخدمة القانونية التي ترغب بها:\n\n"
            "• تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)\n"
            "• تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)\n"
            "• تنظيم العقود الخاصة (100,000 د.ع)\n"
            "• استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)\n",
            reply_markup=reply_markup
        )
        return SERVICE_TYPE
    elif text == "العودة إلى القائمة الرئيسية":
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("عدنا إلى القائمة الرئيسية.", reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text("يرجى اختيار خدمة من القائمة.")

# سنستخدم متغير لتحديد نوع الخدمة والسعر
SERVICE_PRICES = {
    "تنظيم قضايا موظفي الدولة في الوزارات كافة (50,000 د.ع)": 50000,
    "تنظيم قضايا منتسبي الجيش العراقي (50,000 د.ع)": 50000,
    "تنظيم العقود الخاصة (100,000 د.ع)": 50000,
    "استفسارات قانونية أخرى (السعر يُحدد بعد مراجعة المحامي)": None
}

async def service_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in [opt[0] for opt in SERVICE_OPTIONS[:-1]]:
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
        await update.message.reply_text("عدنا إلى القائمة الرئيسية.", reply_markup=reply_markup)
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

user_questions = {}

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
    await context.bot.send_message(chat_id=LAWYER_USER_ID, text=msg)

    await update.message.reply_text(
        "تم إرسال استفسارك للمحامي المختص.\n"
        "سيتم إعلامك عند الموافقة على طلبك."
    )
    return ConversationHandler.END

async def accept_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith("/accept"):
        return
    try:
        question_id = int(text.replace("/accept", ""))
    except ValueError:
        await update.message.reply_text("صيغة رقم الاستفسار غير صحيحة.")
        return

    if question_id in user_questions:
        user_id = user_questions[question_id]["user_id"]
        service_type = user_questions[question_id]["service_type"]
        service_price = user_questions[question_id]["service_price"]
        if service_price is not None:
            accept_message = (
                "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                f"نوع الخدمة: {service_type}\n"
                f"تكلفة الخدمة: {service_price:,} دينار عراقي\n\n"
                "يمكنك الآن إكمال إجراءات الدفع والتواصل عبر أحد الطرق التالية:\n"
                f"1️⃣ تيليجرام: @{LAWYER_USERNAME}\n"
                f"2️⃣ الإيميل: {LAWYER_EMAIL}\n"
                f"3️⃣ واتساب: {LAWYER_WHATSAPP}\n\n"
                "يرجى إرسال صورة التحويل أو رقم العملية عبر الوسيلة التي تفضلها، وسيتم الرد عليك بعد التأكد."
            )
        else:
            accept_message = (
                "✅ تمت الموافقة على استفسارك من قبل المحامي.\n\n"
                f"نوع الخدمة: {service_type}\n"
                "تكلفة الخدمة: سيتم إعلامك بالسعر بعد مراجعة المحامي.\n\n"
                "يمكنك الآن إكمال إجراءات الدفع والتواصل عبر أحد الطرق التالية:\n"
                f"1️⃣ تيليجرام: @{LAWYER_USERNAME}\n"
                f"2️⃣ الإيميل: {LAWYER_EMAIL}\n"
                f"3️⃣ واتساب: {LAWYER_WHATSAPP}\n\n"
                "يرجى إرسال صورة التحويل أو رقم العملية عبر الوسيلة التي تفضلها، وسيتم الرد عليك بعد التأكد."
            )
        await context.bot.send_message(chat_id=user_id, text=accept_message)
        await update.message.reply_text("تم إعلام المستخدم بالموافقة.")
        del user_questions[question_id]
    else:
        await update.message.reply_text("لم يتم العثور على هذا الاستفسار.")

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
    app.add_handler(MessageHandler(filters.Regex(r"^/accept\d+$"), accept_handler))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == '__main__':
    main()