from utils import get_user
from telegram import ReplyKeyboardMarkup
from keyboards import replies


@get_user
async def start(update, context, user):
    message = "Assalamu alaykum, botimizga xush kelibsiz. \nKerakli xizmatni tanlang."

    await update.message.reply_text(
        message,
        reply_markup=replies.get_main(),
    )