import os
from dotenv import load_dotenv

load_dotenv()

import django

from fastapi import FastAPI, Request, HTTPException, Query
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from utils import get_user
from handlers import commands, common, parameters, web
import states

app = FastAPI()


# Store bot applications in a dictionary
applications = {}

CHOOSING, TYPING_REPLY = range(2)



async def choose_option(update, context):
    user_choice = update.message.text
    await update.message.reply_text(f'You chose: {user_choice}. Now, please type your message:')
    return TYPING_REPLY

# Handle user reply
async def handle_reply(update, context):
    user_message = update.message.text
    await update.message.reply_text(f'You typed: {user_message}. Thank you!')
    return ConversationHandler.END

conversation_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text("⚙️ Настройки"), parameters.get_parameters)
    ],
    states={
        states.GET_SETTING: [MessageHandler(filters.TEXT, parameters.get_setting)],
        states.GET_FULL_NAME: [MessageHandler(filters.TEXT, parameters.get_full_name)],
        states.GET_PHONE: [MessageHandler(filters.TEXT, parameters.get_phone)],
    },
    fallbacks=[]
)

order_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web.web_app_data),
        MessageHandler(filters.Text("🛍 Продукты"), web.get_agent_client)
    ],
    states={
        states.CHOOSE_CLIENT: [
            CallbackQueryHandler(web.get_client),
        ],
        states.CHOOSE_PAYMENT: [
            CallbackQueryHandler(web.get_payment)
        ]
    },
    fallbacks=[
        CommandHandler("start", commands.start)
    ]
)

async def setup_bot(token: str):
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(MessageHandler(filters.Text("📞 Связаться с нами"), common.contact))
    application.add_handler(conversation_handler)
    application.add_handler(order_handler)
    
    applications[token] = application

    webhook_url = f"{os.environ.get('WEBHOOK')}webhook?token={token}"
    # await application.bot.set_webhook(url=webhook_url)


@app.on_event("startup")
async def on_startup():
    bot_tokens = os.environ.get("TOKENS").split(",")
    
    for token in bot_tokens:
        await setup_bot(token)


@app.post("/webhook")
async def handle_update(request: Request, token: str = Query(...)):
    print(applications)
    if token not in applications:
        raise HTTPException(status_code=404, detail="Invalid bot token")

    application = applications[token]
    data = await request.json()

    update = Update.de_json(data, application.bot)
    await application.initialize()
    await application.process_update(update)
    
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT")))