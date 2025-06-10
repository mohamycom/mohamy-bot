from telegram import InlineKeyboardMarkup, InlineKeyboardButton

MAIN_MENU = [
    ["خدماتنا المدفوعة"],
    ["عن (محامي.كوم)"]
]

BACK_TO_MENU = [["العودة إلى القائمة الرئيسية"]]

ONLY_BACK_MARKUP = MAIN_MENU_MARKUP = None  # سيتم ضبطها ديناميكياً إذا احتجت ذلك

PAID_REPLY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton("نعم، أوافق", callback_data="agree_paid")],
    [InlineKeyboardButton("العودة إلى القائمة الرئيسية", callback_data="back_to_menu")]
])

SERVICE_OPTIONS = [
    ["استشارة قانونية مكتوبة"],
    ["استشارة قانونية صوتية"],
    ["مكالمة هاتفية مع المحامي"],
    ["خدمة أخرى"]
]

def get_lawyer_approval_markup(question_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("قبول الاستفسار", callback_data=f"approve_{question_id}"),
            InlineKeyboardButton("رفض الاستفسار", callback_data=f"reject_{question_id}")
        ]
    ])

def get_contact_markup(question_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("تواصل عبر التليجرام", callback_data=f"contact_telegram_{question_id}")],
        [InlineKeyboardButton("تواصل عبر الواتساب", callback_data=f"contact_whatsapp_{question_id}")],
        [InlineKeyboardButton("تواصل عبر البريد الإلكتروني", callback_data=f"contact_email_{question_id}")]
    ])