from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.models import Order

def get_user_inline_keyboard(users):
    keyboard = []
    for user in users:
        button = InlineKeyboardButton(text=f"{user.first_name} {user.last_name}", callback_data=f"order_{user.id}")
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


def create_payment_keyboard():
    PaymentTypes = Order.PaymentTypes
    keyboard = [
        [InlineKeyboardButton(PaymentTypes.CASH.label, callback_data=PaymentTypes.CASH.value)],
        [InlineKeyboardButton(PaymentTypes.PAYME.label, callback_data=PaymentTypes.PAYME.value)],
        [InlineKeyboardButton(PaymentTypes.CLICK.label, callback_data=PaymentTypes.CLICK.value)],
        [InlineKeyboardButton(PaymentTypes.TERMINAL.label, callback_data=PaymentTypes.TERMINAL.value)],
        [InlineKeyboardButton(PaymentTypes.OTHER.label, callback_data=PaymentTypes.OTHER.value)]
    ]
    return InlineKeyboardMarkup(keyboard)