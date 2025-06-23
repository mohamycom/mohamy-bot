import time
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from config import (
    WELCOME_MESSAGE, ABOUT_MESSAGE, LAWYER_USER_ID, LAWYER_USERNAME, ACCOUNT_NUMBER,
    SERVICE_PRICES, SERVICE_NAMES_DISPLAY, SPAM_WAIT_SECONDS, LAWYER_WHATSAPP, LAWYER_EMAIL
)
from keyboards import (
    MAIN_MENU, BACK_TO_MENU, PAID_REPLY_MARKUP, ONLY_BACK_MARKUP,
    SERVICE_OPTIONS, get_contact_markup, get_lawyer_approval_markup
)
from database import (
    save_question, get_question_by_id, get_all_questions, get_last_question_time, delete_question
)
from states_enum import States

CHANNEL_USERNAME = "mohamycom_tips"  # اسم قناتك بدون @

def is_spam_per_action(update, context, action_name):
    user_id = update.effective_user.id
    if user_id == LAWYER_USER_ID:
        return False
    now = int(time.time())
    last_action = context.user_data.get(f'last_action_time_{action_name}', 0)
    if now - last_action < 15:
        return True
    context.user_data[f'last_action_time_{action_name}'] = now
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = context.bot_data.get('main_menu_markup')
    if not reply_markup:
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        context.bot_data['main_menu_markup'] = reply_markup
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, protect_content=True)
    context.user_data.clear()

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    button_map = {
        "استشارات فورية": "fast_consult",
        "نصائح وارشادات قانونية": "tips",
        "تواصل مع محامي": "contact_lawyer",
        "عن (محاميكم)": "about",
        "العودة إلى القائمة الرئيسية": "main_menu"
    }
    action_name = button_map.get(text, "other_menu")
    if text != "العودة إلى القائمة الرئيسية" and is_spam_per_action(update, context, action_name):
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("يرجى الانتظار 15 ثانية قبل إعادة المحاولة.", reply_markup=reply_markup, protect_content=True)
        return ConversationHandler.END

    if text == "العودة إلى القائمة الرئيسية":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, protect_content=True)
        context.user_data.clear()
        return ConversationHandler.END
    elif text == "عن (محاميكم)":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(BACK_TO_MENU, resize_keyboard=True)
        await update.message.reply_text(ABOUT_MESSAGE, reply_markup=reply_markup, protect_content=True)
        return ConversationHandler.END
    elif text == "تواصل مع محامي":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True)
        await update.message.reply_text(
            "🟢 الخدمة المدفوعة - استشارة خاصة\n\n"
            "-  هذه الخدمة خاصة ، من خلال التواصل مع محامي مختص يمكنك استعراض كافة وقائع الاستفسار للحصول على استشارة دقيقة ومحددة.\n\n"
            "اختر من القائمة أدناه نوع الخدمة بالتحديد:",
            reply_markup=reply_markup,
            protect_content=True
        )
        return States.SERVICE_TYPE
    elif text == "نصائح وارشادات قانونية":
        url = f"https://t.me/{CHANNEL_USERNAME}"
        await update.message.reply_text(
            "اضغط أدناه لرؤية مختلف النصائح القانونية:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("الدخول للقناة", url=url)]
            ]),
            protect_content=True
        )
        return ConversationHandler.END
    elif text == "استشارات فورية":
        url = "https://t.me/IrMoLaBot"
        await update.message.reply_text(
            "للحصول على استشارة قانونية فورية مباشرة، اضغط الزر أدناه للدخول إلى المنصة:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("الدخول إلى منصة الاستشارات", url=url)]
            ]),
            protect_content=True
        )
        return ConversationHandler.END
    elif text in sum(MAIN_MENU, []):
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(BACK_TO_MENU, resize_keyboard=True)
        await update.message.reply_text("سيتم تفعيل الخدمة قريبا", reply_markup=reply_markup, protect_content=True)
        return ConversationHandler.END
    else:
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(❗️عذراً، لم أفهم طلبك. يرجى اختيار أحد الخيارات من القائمة بالأسفل.", reply_markup=reply_markup, protect_content=True)
        return ConversationHandler.END

async def service_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    action_name = text
    if text != "العودة إلى القائمة الرئيسية" and is_spam_per_action(update, context, action_name):
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True)
        await update.message.reply_text("يرجى الانتظار 15 ثانية قبل إعادة المحاولة.", reply_markup=reply_markup, protect_content=True)
        return States.SERVICE_TYPE

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
            "- هذه الخدمة خاصة ، من خلال التواصل مع محامي مختص يمكنك استعراض كافة وقائع الاستفسار للحصول على استشارة دقيقة ومحددة.\n"
            f"{price_msg}\n"
            "هل توافق على الشروط وتريد متابعة طلب الاستشارة؟",
            reply_markup=PAID_REPLY_MARKUP,
            protect_content=True
        )
        return States.PAID_SERVICE
    elif text == "العودة إلى القائمة الرئيسية":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, protect_content=True)
        context.user_data.clear()
        return ConversationHandler.END
    else:
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(SERVICE_OPTIONS, resize_keyboard=True)
        await update.message.reply_text("يرجى اختيار نوع خدمة من القائمة أو العودة.", reply_markup=reply_markup, protect_content=True)
        return States.SERVICE_TYPE

async def paid_service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    action_name = text
    if text not in ["العودة إلى القائمة الرئيسية", "إلغاء"] and is_spam_per_action(update, context, action_name):
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(PAID_REPLY_MARKUP.keyboard, resize_keyboard=True)
        await update.message.reply_text("يرجى الانتظار 15 ثانية قبل إعادة المحاولة.", reply_markup=reply_markup, protect_content=True)
        return States.PAID_SERVICE

    if text == "نعم، أوافق":
        await update.message.reply_text(
            "يرجى ملاحظة ما يلي:\n"
            "1. ان طريقة الدفع تتم في الوقت الحالي عبر تطبيق (سوبر كي) المدعوم من قبل مصرف الرافدين ولاتتوفر طريقة دفع اخرى .\n"
            "2. يرجى كتابة  الاستفسار كاملا برسالة واحدة وعدم اجتزاءه برسائل متعددة.\n"
            "3. ستتم مراجعة الاستفسار من قبل محامين متخصصين وفي حال الموافقة سيتم ارسال اشعار اليكم بذلك متضمنا كيفية الدفع .\n"
            "شكرا لتفهمكم",
            reply_markup=ONLY_BACK_MARKUP,
            protect_content=True
        )
        return States.WAITING_QUESTION
    elif text == "العودة إلى القائمة الرئيسية":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, protect_content=True)
        context.user_data.clear()
        return ConversationHandler.END
    else:
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("تم إلغاء الطلب.", reply_markup=reply_markup, protect_content=True)
        context.user_data.clear()
        return ConversationHandler.END

async def question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    action_name = "question"
    if text != "العودة إلى القائمة الرئيسية" and is_spam_per_action(update, context, action_name):
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("يرجى الانتظار 15 ثانية قبل إعادة المحاولة.", reply_markup=reply_markup, protect_content=True)
        return ConversationHandler.END

    if text == "العودة إلى القائمة الرئيسية":
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, protect_content=True)
        context.user_data.clear()
        return ConversationHandler.END

    user = update.message.from_user
    chat_id = update.message.chat_id

    last_time = get_last_question_time(chat_id)
    now = int(time.time())
    if last_time and (now - last_time) < SPAM_WAIT_SECONDS:
        from telegram import ReplyKeyboardMarkup
        reply_markup = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text(
            "لقد أرسلت استفسارًا مؤخرًا. يرجى الانتظار 5 دقائق قبل إرسال استفسار جديد.",
            reply_markup=reply_markup,
            protect_content=True
        )
        context.user_data.clear()
        return ConversationHandler.END

    question = text
    service_type = context.user_data.get("selected_service_type", "غير محدد")
    service_price = SERVICE_PRICES.get(service_type)
    service_display = SERVICE_NAMES_DISPLAY.get(service_type, service_type)

    question_id = save_question(chat_id, question, service_type, service_price, now)

    lawyer_markup = get_lawyer_approval_markup(question_id)

    msg = (
        f"استفسار مدفوع جديد\n"
        f"رقم الاستفسار: {question_id}\n"
        f"نوع الخدمة: {service_display}\n"
        f"من: {user.full_name} (@{user.username or 'بدون يوزرنيم'})\n"
        f"نص الاستفسار:\n{question}\n\n"
        f"يرجى اختيار الإجراء:"
    )
    await update.message.reply_text(
        "تم إرسال استفسارك للمحامي المختص.\n"
        "سيتم إعلامك عند الموافقة على طلبك.\n\n"
        "⛔️ ملاحظة: يحظر نسخ محتوى الاستشارات القانونية.",
        reply_markup=ONLY_BACK_MARKUP,
        protect_content=True
    )
    await context.bot.send_message(chat_id=LAWYER_USER_ID, text=msg, reply_markup=lawyer_markup, protect_content=True)
    context.user_data.clear()
    return ConversationHandler.END

async def lawyer_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    if user_id != LAWYER_USER_ID:
        if data.startswith("contact_"):
            action_name = data.split("_")[1]
            now = int(time.time())
            last_contact = context.user_data.get(f'last_action_time_contact_{action_name}', 0)
            if now - last_contact < 15:
                await query.answer("يرجى الانتظار 15 ثانية قبل المحاولة مرة أخرى.", show_alert=True)
                return
            context.user_data[f'last_action_time_contact_{action_name}'] = now

    if (data.startswith("approve_") or data.startswith("reject_")) and query.from_user.id != LAWYER_USER_ID:
        await query.answer("غير مصرح لك بهذا الإجراء", show_alert=True)
        return

    if data.startswith("approve_"):
        question_id = int(data.replace("approve_", ""))
        q = get_question_by_id(question_id)
        if q:
            user_id = q["user_id"]
            service_type = q["service_type"]
            service_price = q["service_price"]
            service_display = SERVICE_NAMES_DISPLAY.get(service_type, service_type)
            contact_markup = get_contact_markup(question_id)
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
                await context.bot.send_message(
                    chat_id=user_id,
                    text=accept_message,
                    reply_markup=contact_markup,
                    protect_content=True
                )
            except Exception as e:
                await query.edit_message_text(f"حدث خطأ أثناء محاولة إرسال رسالة القبول للمستخدم: {e}", protect_content=True)
                return
            await query.edit_message_text("تم إعلام المستخدم بالموافقة.", protect_content=True)
            delete_question(question_id)
        else:
            await query.edit_message_text("لم يتم العثور على هذا الاستفسار.", protect_content=True)
        return

    elif data.startswith("reject_"):
        question_id = int(data.replace("reject_", ""))
        q = get_question_by_id(question_id)
        if q:
            user_id = q["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ تم رفض استفسارك من قبل المحامي.\n\n"
                    f"إذا كنت تعتقد أن هناك خطأ أو لديك أي استفسار، يرجى مراسلة حسابنا على التليجرام:\n@{LAWYER_USERNAME}",
                reply_markup=ONLY_BACK_MARKUP,
                protect_content=True
            )
            delete_question(question_id)
            await query.edit_message_text("تم إرسال إشعار الرفض للمستخدم.", protect_content=True)
        else:
            await query.edit_message_text("لم يتم العثور على هذا الاستفسار.", protect_content=True)
        return

    if data.startswith("contact_"):
        try:
            parts = data.split("_", 2)
            method = parts[1]
            if method == "telegram":
                text = f"اضغط هنا للتواصل عبر التليجرام:\nhttps://t.me/{LAWYER_USERNAME}"
            elif method == "whatsapp":
                number = LAWYER_WHATSAPP.strip().replace("+", "").replace(" ", "")
                if not re.match(r'^[0-9]{8,15}$', number):
                    await query.message.reply_text("رقم الواتساب غير صحيح.", protect_content=True)
                    return
                if number.startswith("0"):
                    number = "964" + number[1:]
                elif not number.startswith("964"):
                    number = "964" + number
                text = f"اضغط هنا للتواصل عبر الواتساب:\nhttps://wa.me/{number}"
            elif method == "email":
                text = f"اضغط هنا لإرسال بريد إلكتروني:\nmailto:{LAWYER_EMAIL}"
            else:
                text = "طريقة التواصل غير معروفة."
            await query.message.reply_text(text, protect_content=True)
        except Exception as e:
            await query.message.reply_text(f"حدث خطأ داخلي: {e}", protect_content=True)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"حدث خطأ: {context.error}")