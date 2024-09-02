from functools import wraps
from telegram import Update
from bot.models import TelegramUser
from asgiref.sync import sync_to_async

def get_user(handler):
    @wraps(handler)
    async def wrapper(update: Update, context, *args, **kwargs):
        user = update.effective_user
        user_data = {
            'telegram_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        try:
            user = await TelegramUser.objects.prefetch_related("territory").aget(telegram_id=user.id)
            user.username = user_data.get("username", "")
            if not user.is_updated:
                user.first_name = user_data.get("first_name", "")
                user.last_name = user_data.get("last_name", "")

            await user.asave()
        except Exception as e:
            print(e)
            user = await TelegramUser.objects.acreate(**user_data)
        
        return await handler(update, context, user, *args, **kwargs)
    
    return wrapper


async def get_solo(model):
    return await sync_to_async(model.get_solo)()


@sync_to_async
def update_or_create(model, params, defaults):
    obj, created = model.objects.update_or_create(**params, defaults=defaults)
    return obj, created