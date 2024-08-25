from telegram import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def get_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    text="🛍 Mahsulotlar",
                    web_app=WebAppInfo(url="https://gpadmin.joseph.uz/webapp"),
                )
            ],
            [
                KeyboardButton(text="📞 Biz bilan bog'laning")
            ],
            [
                KeyboardButton(text="⚙️ Sozlamalar")
            ]

        ],
        resize_keyboard=True,
    )



def get_settings():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="🪪 Ism va Familiyani tahrirlash"), KeyboardButton(text="📞 Telefon raqamni tahrirlash")
            ],
            [
                KeyboardButton(text="◀️ Ortga qaytish")
            ]
        ], resize_keyboard=True
    )


def get_back():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="◀️ Ortga qaytish", )
            ]
        ], resize_keyboard=True
    )