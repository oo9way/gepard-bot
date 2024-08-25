from django.contrib import admin
from bot.models import TelegramUser, Contact, Product
from solo.admin import SingletonModelAdmin

admin.site.register(TelegramUser)
admin.site.register(Contact, SingletonModelAdmin)
admin.site.register(Product)