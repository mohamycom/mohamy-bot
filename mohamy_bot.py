import os
import asyncio
import threading
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
TOKEN = os.environ.get('TOKEN')

# ===== تطبيق Flask لاشتراطات Render =====
app = Flask(__name__)

@app.route('/')
def health_check():
    return "✅ البوت يعمل بنجاح | Mohamy Bot", 200

# ===== لوحات المفاتيح الكاملة =====
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

# ===== معالجة الأوامر الكاملة =====
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
        context.user_data['service'] = "صياغة العقود الشخصية والحكومية"
        context.user_data['price'] = 150
        await update.message.reply_text(
            "📝 **خدمة صياغة العقود**\n\n"
            "السعر: 150 ريال\n"
            "هل تريد المتابعة للدفع؟",
            reply_markup=payment_confirmation_keyboard(),
            parse_mode="Markdown"
        )
    
    elif text == "نعم، اريد المتابعة للدفع":
        service = context.user_data.get('service', '')
        price = context.user_data.get('price', 0)
        if service and price > 0:
            payment_link = f"https://payment.mohamy.com/?service={service.replace(' ', '_')}&amount={price}"
            await update.message.reply_text(
                f"⚡ رابط الدفع الآمن:\n{payment_link}",
                reply_markup=ReplyKeyboardRemove()
            )
    
    elif text == "تواصل مع فريق المحامين":
        await update.message.reply_text(
            "📞 للتواصل:\n"
            "واتساب: +9647775535047\n"
            "ساعات العمل: 6م-10م"
        )
    
    elif text in ["لا، شكراً", "العودة للرئيسية"]:
        await update.message.reply_text(
            "تم العودة للقائمة الرئيسية",
            reply_markup=main_keyboard()
        )

# ===== إعدادات التشغيل المحسنة =====
async def cleanup():
    app = Application.builder().token(TOKEN).build()
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("🔄 تم تنظيف الجلسات السابقة")

def run_flask():
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

async def run_bot():
    try:
        application = Application.builder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        await cleanup()
        print("🚀 البوت يعمل الآن!")
        await application.run_polling()
    except Exception as e:
        print(f"❌ خطأ: {e}")
        await asyncio.sleep(5)
        await run_bot()

def main():
    # تشغيل Flask في خيط منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل البوت في الخيط الرئيسي
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()