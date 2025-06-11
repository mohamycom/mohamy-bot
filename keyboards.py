from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

MAIN_MENU = [
    ["استشارات قانونية (تلقائية)", "خدماتنا المدفوعة"],
    ["نصائح وارشادات قانونية", "عن (محامي.كوم)"]
]

BACK_TO_MENU = [[KeyboardButton("العودة إلى القائمة الرئيسية")]]
PAID_REPLY_MARKUP = ReplyKeyboardMarkup([["نعم، أوافق"], ["إلغاء"], ["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)
ONLY_BACK_MARKUP = ReplyKeyboardMarkup([["العودة إلى القائمة الرئيسية"]], resize_keyboard=True)

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

# أزرار أقسام نصائح القناة (كل 2 في صف)
LEGAL_TIPS_BUTTONS = [
    ["الاحوال الشخصية", "الجرائم والعقوبات"],
    ["العقود والاتفاقيات", "العقارات والممتلكات"],
    ["السيارات والمرور", "القروض والديون"],
    ["السفر والجوازات", "حقوق المستهلك"],
    ["الشكاوى والتظلمات", "نصائح عامة"],  # <-- هنا تم تغيير الاسم
    ["تصفح جميع النصائح القانونية"],
    ["العودة إلى القائمة الرئيسية"]
]

def get_contact_markup(question_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("التواصل عبر التليجرام", callback_data=f"contact_telegram_{question_id}")],
        [InlineKeyboardButton("التواصل عبر الواتساب", callback_data=f"contact_whatsapp_{question_id}")],
        [InlineKeyboardButton("التواصل عبر الايميل", callback_data=f"contact_email_{question_id}")]
    ])

def get_lawyer_approval_markup(question_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("موافقة", callback_data=f"approve_{question_id}"),
            InlineKeyboardButton("رفض", callback_data=f"reject_{question_id}")
        ]
    ])