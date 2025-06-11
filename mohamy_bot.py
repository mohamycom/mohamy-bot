from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, CallbackQueryHandler, filters
)
from handlers import (
    start, menu_handler, service_type_handler, paid_service_handler,
    question_handler, lawyer_callback_handler, error_handler, legal_tips_handler
)
from keyboards import MAIN_MENU
from config import TOKEN
from states_enum import States
from database import init_db  # الآن استورد من database.py (Postgres)

def main():
    init_db()  # تهيئة قاعدة البيانات عند التشغيل

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
        states={
            States.SERVICE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_type_handler)],
            States.PAID_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, paid_service_handler)],
            States.WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_handler)],
            States.LEGAL_TIPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, legal_tips_handler)],
        },
        fallbacks=[MessageHandler(filters.Regex("^العودة إلى القائمة الرئيسية$"), menu_handler)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(lawyer_callback_handler, pattern=r"^(approve_|reject_|contact_).*"))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == '__main__':
    main()