import os
from dotenv import load_dotenv

load_dotenv()

from telegram import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def get_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    text="🛍 Продукты",
                    web_app=WebAppInfo(url=os.environ.get("WEBAPP")),
                )
            ],
            [
                KeyboardButton(text="📞 Связаться с нами")
            ],
            [
                KeyboardButton(text="⚙️ Настройки")
            ]

        ],
        resize_keyboard=True,
    )

def get_agent_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(
                    text="🛍 Продукты",
                )
            ],
            [
                KeyboardButton(text="📞 Связаться с нами")
            ],
            [
                KeyboardButton(text="⚙️ Настройки")
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