from utils import get_user, update_or_create
from keyboards import replies, inlines
import json
from telegram import Update
from telegram.ext import CallbackContext
from bot.models import TelegramUser, Order, OrderItem, Product
import states
from asgiref.sync import sync_to_async
from django.db.models import Q

# async def get_telegram_users(user):
#     from django.db import close_old_connections
#     close_old_connections()
#     return await sync_to_async(lambda: TelegramUser.objects.filter(territory__in=user.territory.all(), is_agent=False))()

async def fetch_clients(territories):
    # Wrap the ORM operation with sync_to_async
    return await sync_to_async(lambda: list(TelegramUser.objects.filter(territory__in=territories, is_agent=False)))()

@get_user
async def web_app_data(update: Update, context: CallbackContext, user: TelegramUser) -> None:
    data = json.loads(update.effective_message.web_app_data.data)

    if not user.is_agent:
        await update.message.reply_html(
            text="Sizda buyurtma berish ruxsati mavjud emas. \nKerakli xizmatni tanlang",
            reply_markup=replies.get_main()
        )
        return -1
    
    order = await Order.objects.acreate(user=user)
    order_items = []
    
    for item in data:
        try:
            product = await Product.objects.aget(id=item['id'])
            order_items.append(
                OrderItem(
                    order=order,
                    product_name=product.title,
                    qty=item['qty'],
                    price_uzs=item['price_uzs'],
                    price_usd=item['price_usd']
                )
            )

        except Product.DoesNotExist:
            continue

    if order_items:
        await OrderItem.objects.abulk_create(order_items)
    territories = await sync_to_async(user.territory.all)()
    clients = await fetch_clients(territories)
    if not clients:
        message = "Заказ отменен, так как у вас нет клиентов"
        await order.adelete()
        await update.message.reply_text(message, reply_markup=replies.get_main())
        return -1

    message = "Выберите клиента"
    await update.message.reply_text(message, reply_markup=inlines.get_user_inline_keyboard(clients))


    context.user_data["uncompleted_order_id"] = order.pk
    return states.CHOOSE_CLIENT

    # message = "<b>📦 Buyurtma muvaffaqiyatli berildi.</b> \n"
    # message += "📄 Buyurtma holati: <b>Kutilmoqda </b>\n\n"
    # message += "====================================\n\n"
    # total_price = 0
    # for idx, item in enumerate(order_items):
    #     total_price += int(item.qty) * int(item.price)
    #     message += f"<b>{idx + 1}. {item.product_name} ({item.qty}x{item.price} so'm)</b>\n"

    # message += "\n====================================\n\n"
    # message += f"<b>💰 Umumiy {total_price} so'm</b>"
    

    # await update.message.reply_html(
    #     text=message,
    #     reply_markup=replies.get_main(),
    # )


@get_user
async def get_client(update: Update, context: CallbackContext, user:TelegramUser) -> None:
    data = update.callback_query.data
    client_id = data.split("_")[1]
    client = await TelegramUser.objects.aget(id=client_id)
    order = await Order.objects.aget(id=context.user_data['uncompleted_order_id'])
    order.user = client
    order.agent = user
    order.asave()

    await update.callback_query.answer()
    message = "Выберите тип оплаты"
    await update.callback_query.message.reply_text(message, reply_markup=inlines.create_payment_keyboard())
    await update.callback_query.delete_message()
    return states.CHOOSE_PAYMENT


@get_user
async def get_payment(update: Update, context: CallbackContext, user:TelegramUser):
    data = update.callback_query.data
    order = await Order.objects.aget(id=context.user_data['uncompleted_order_id'])
    order.payment_type = data
    print(order.id, "OOOOOOEEEERRRDERRR")
    await order.asave()
    await update.callback_query.delete_message()


    message = "Заказ выполнен успешно"
    await update.callback_query.message.reply_text(message)
    return -1


    