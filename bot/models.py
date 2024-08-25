from django.db import models
from solo.models import SingletonModel

class TelegramUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_agent = models.BooleanField(default=False)
    phone = models.CharField(null=True, blank=True, max_length=255)
    is_updated = models.BooleanField(editable=False, default=False)

    def get_full_name(self):
        first_name = self.first_name if self.first_name else ""
        last_name = self.last_name if self.last_name else ""

        return f"{first_name} {last_name}"
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Contact(SingletonModel):
    body = models.TextField("Matn")

    class Meta:
        verbose_name = "📞  Biz bilan bog'laning"
        verbose_name_plural = "📞  Biz bilan bog'laning"


class Product(models.Model):
    cover = models.ImageField("Mahsulot rasmi", upload_to="products")
    title = models.CharField("Mahsulot nomi", max_length=255)
    description = models.TextField("Izoh")
    is_active = models.BooleanField("Faolmi ?", default=True)
    price = models.IntegerField("Narxi", default=0)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"



class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Yangi"
        APPROVED_BY_ACCOUNTANT = "approved_by_account", "Hisobchi tomonidan tasdiqlangan"
        APPROVED_BY_DIRECTOR = "approved_by_director", "Direktor tomonidan tasdiqlangan"
        APPROVED_BY_STOREKEEPER = "approved_by_storekeeper", "Omborchi tomonidan tasdiqlangan"
    user = models.ForeignKey(verbose_name="Mijoz", to=TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField("Buyurtma holati", max_length=24, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField("Buyurtma berilgan vaqt", auto_now=True)
    accountant_approve_time = models.DateTimeField("Hisobchi tasdiqlagan vaqt", null=True, blank=True)
    director_approve_time = models.DateTimeField("Direktor tasdiqlagan vaqt", null=True, blank=True)
    storekeeper_approve_time = models.DateTimeField("Omborchi tasdiqlagan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"



class OrderItem(models.Model):
    order = models.ForeignKey(verbose_name="Buyurtma", to=Order, on_delete=models.CASCADE)
    product_name = models.CharField("Mahsulot nomi", max_length=255)
    qty = models.IntegerField("Soni", default=0)
    price = models.IntegerField("Narxi", default=0)

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"