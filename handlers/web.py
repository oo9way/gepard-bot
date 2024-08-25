from utils import get_user, update_or_create
from keyboards import replies
import json
from telegram import Update
from telegram.ext import CallbackContext
from bot.models import TelegramUser, Order, OrderItem, Product

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
                    qty=int(item['qty']),
                    price=int(item['price'])
                )
            )

        except Product.DoesNotExist:
            continue

    if order_items:
        await OrderItem.objects.abulk_create(order_items)

    message = "<b>📦 Buyurtma muvaffaqiyatli berildi.</b> \n"
    message += "📄 Buyurtma holati: <b>Kutilmoqda </b>\n\n"
    message += "====================================\n\n"
    total_price = 0
    for idx, item in enumerate(order_items):
        total_price += int(item.qty) * int(item.price)
        message += f"<b>{idx + 1}. {item.product_name} ({item.qty}x{item.price} so'm)</b>\n"

    message += "\n====================================\n\n"
    message += f"<b>💰 Umumiy {total_price} so'm</b>"
    

    await update.message.reply_html(
        text=message,
        reply_markup=replies.get_main(),
    )