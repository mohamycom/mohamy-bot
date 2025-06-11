from telegram import ReplyKeyboardMarkup, KeyboardButton

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