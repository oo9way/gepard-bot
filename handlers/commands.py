from utils import get_user
from telegram import ReplyKeyboardMarkup
from keyboards import replies


@get_user
async def start(update, context, user):
    message = "Здравствуйте, добро пожаловать в наш бот. \nВыберите нужную услугу."

    if user.is_agent:
        return await update.message.reply_text(
            message, reply_markup=replies.get_agent_main()
        )
    return await update.message.reply_text(message,reply_markup=replies.get_main())
    
    