from import_export import resources
from bot.models import TelegramUser


class UsersTableResourse(resources.ModelResource):

    def dehydrate_is_agent(self, obj):
        if obj.is_agent:
            return "Да"
        return "Нет"
    
    def dehydrate_is_active(self, obj):
        if obj.is_active:
            return "Да"
        return "Нет"
    
    def dehydrate_category(self, obj):
        if obj.category:
            return obj.category.name
        return "Нет"
    
    def dehydrate_territory(self, obj):
        if obj.territory:
            return obj.territory.name
        return "Нет"
    
    class Meta:
        model = TelegramUser
        exclude = ("id", "telegram_id", "username", "is_updated")

    def get_export_headers(self, fields=None):
        return ['Имя', 'Фамилия', 'Агент', 'Активен', 'Номер телефона', 'ИНН', 'Категория', 'Территория']
        
