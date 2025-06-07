import os
import asyncio
import threading
import time
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== إعدادات التوكن =====
TOKEN = os.environ.get('TOKEN')  # يُسحب من متغيرات البيئة في Render

# ===== تطبيق Flask لاشتراطات Render =====
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running in polling mode", 200

# ===== لوحات المفاتيح =====
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

# ===== معالجة الأوامر =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """🔒 **مرحبًا بك في بوت محامي.كوم** ⚖️

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
            "السعر: 150 ريال\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "تنظيم قضايا":
        context.user_data['selected_service'] = "تنظيم قضايا"
        context.user_data['service_price'] = 500
        
        await update.message.reply_text(
            "⚖️ **خدمة تنظيم قضايا**\n\n"
            "السعر: 500 ريال\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "استشارة خاصة":
        context.user_data['selected_service'] = "استشارة خاصة"
        context.user_data['service_price'] = 200
        
        await update.message.reply_text(
            "👨⚖️ **استشارة خاصة**\n\n"
            "السعر: 200 ريال\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "نعم، اريد المتابعة للدفع":
        service = context.user_data.get('selected_service', '')
        price = context.user_data.get('service_price', 0)
        
        if service and price > 0:
            payment_link = f"https://payment.mohamy.com/?service={service.replace(' ', '_')}&amount={price}"
            await update.message.reply_text(
                f"🔐 **تفاصيل الدفع**\n\n"
                f"الخدمة: {service}\n"
                f"المبلغ: {price} ريال\n\n"
                f"للاستمرار، يرجى الدفع عبر الرابط الآمن:\n{payment_link}",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="Markdown"
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
            "ساعات العمل: 6م-10م"
        )
    
    elif text == "عن محامي . كوم":
        await update.message.reply_text(
            "⚖️ محامي.كوم - المنصة القانونية الرائدة\n"
            "تأسست عام 2025\n"
            "فريق من 13 محامي معتمد"
        )

# ===== إعدادات التشغيل الآمن =====
async def cleanup_before_start(app: Application):
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("✅ تم تنظيف جميع النسخ السابقة")
    await asyncio.sleep(2)

async def run_bot():
    try:
        application = (
            Application.builder()
            .token(TOKEN)
            .post_init(cleanup_before_start)
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print("🚀 بدء تشغيل البوت...")
        await application.run_polling(
            drop_pending_updates=True,
            timeout=30,
            close_loop=False,
            allowed_updates=Update.ALL_TYPES
        )
    except Exception as e:
        print(f"❌ خطأ: {e}")
        await asyncio.sleep(5)
        await run_bot()

# ===== التشغيل الرئيسي =====
if __name__ == "__main__":
    # تشغيل Flask في خلفية منفصلة
    flask_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)
    )
    flask_thread.daemon = True
    flask_thread.start()

    # تشغيل البوت الرئيسي
    asyncio.run(run_bot())