from django.db import models
from solo.models import SingletonModel
from django.contrib.auth.models import AbstractUser, Group
from django.core.management import call_command
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('director', 'Direktor'),
        ('accountant', 'Hisobchi'),
        ('storekeeper', 'Omborchi'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Menedjer"
        verbose_name_plural = "Menedjerlar"

    def save(self, *args, **kwargs):
        call_command('generate_permissions')

        if not self.pk:
            self.password = make_password(self.password)
            self.is_active = True
            self.is_staff = True
            super().save(*args, **kwargs)

        if not self.is_superuser:
            if self.role == "director" or self.role == "accountant":
                groups = Group.objects.filter(name="default")
                self.groups.set(groups)
            else:
                groups = Group.objects.filter(name="keeper")
                self.groups.set(groups)
            

    def __str__(self):
        return self.username



class TelegramUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField("Ismi", max_length=255, blank=True, null=True)
    last_name = models.CharField("Familiyasi", max_length=255, blank=True, null=True)
    is_agent = models.BooleanField("Agentmi ?", default=False)
    phone = models.CharField("Telefon raqam", null=True, blank=True, max_length=255)
    is_updated = models.BooleanField(editable=False, default=False)

    def get_full_name(self):
        first_name = self.first_name if self.first_name else ""
        last_name = self.last_name if self.last_name else ""

        return f"{first_name} {last_name}"
    
    def __str__(self) -> str:
        return self.get_full_name()
    
    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"


class Contact(SingletonModel):
    body = models.TextField("Matn")

    class Meta:
        verbose_name = "Biz bilan bog'laning"
        verbose_name_plural = "Biz bilan bog'laning"


class Category(models.Model):
    cover = models.ImageField("Kategoriya rasmi", upload_to="categories")
    title = models.CharField("Kategoriya nomi", max_length=255)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    cover = models.ImageField("Mahsulot rasmi", upload_to="products")
    title = models.CharField("Mahsulot nomi", max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="products", 
        verbose_name="Kategoriya"
    )
    description = models.TextField("Izoh")
    is_active = models.BooleanField("Faolmi ?", default=True)
    price_uzs = models.IntegerField("Narxi (so'm)", default=0)
    price_usd = models.IntegerField("Narxi (USD)", default=0)
    amount = models.IntegerField("Soni", default=0)
    is_top = models.BooleanField("Ommabop mahsulot", default=False)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"



class Order(models.Model):
    class PaymentTypes(models.TextChoices):
        CASH = "cash", "Naqd"
        PAYME = "payme", "Payme"
        CLICK = "click", "Click"
        TERMINAL = "terminal", "Terminal"
        OTHER = "other", "Boshqa"

    class PaymentStatus(models.TextChoices):
        PAID = "paid", "To'langan"
        UNPAID = "unpaid", "To'lanmagan"

    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Yangi"
        APPROVED_BY_ACCOUNTANT = "approved_by_account", "Hisobchi tomonidan tasdiqlangan"
        APPROVED_BY_DIRECTOR = "approved_by_director", "Direktor tomonidan tasdiqlangan"
        APPROVED_BY_STOREKEEPER = "approved_by_storekeeper", "Omborchi tomonidan tasdiqlangan"

    class DirectorStatus(models.TextChoices):
        APPROVED_BY_ACCOUNTANT = "approved_by_account", "Hisobchi tomonidan tasdiqlangan"
        APPROVED_BY_DIRECTOR = "approved_by_director", "Direktor tomonidan tasdiqlangan"

    class AccountantStatus(models.TextChoices):
        PENDING = "pending", "Yangi"
        APPROVED_BY_ACCOUNTANT = "approved_by_account", "Hisobchi tomonidan tasdiqlangan"

    class StoreKeeperStatus(models.TextChoices):
        APPROVED_BY_DIRECTOR = "approved_by_director", "Direktor tomonidan tasdiqlangan"
        APPROVED_BY_STOREKEEPER = "approved_by_storekeeper", "Omborchi tomonidan tasdiqlangan"

    user = models.ForeignKey(verbose_name="Mijoz", to=TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField("To'lov holati", choices=PaymentStatus.choices, default=PaymentStatus.UNPAID, max_length=16)
    payment_type = models.CharField("To'lov turi", choices=PaymentTypes.choices, null=True, blank=True, max_length=16)
    status = models.CharField("Buyurtma holati", max_length=24, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField("Buyurtma berilgan vaqt", auto_now=True)
    accountant_approve_time = models.DateTimeField("Hisobchi tasdiqlagan vaqt", null=True, blank=True)
    director_approve_time = models.DateTimeField("Direktor tasdiqlagan vaqt", null=True, blank=True)
    storekeeper_approve_time = models.DateTimeField("Omborchi tasdiqlagan vaqt", null=True, blank=True)

    def clean(self) -> None:
        from django.core.exceptions import ValidationError
        if self.payment_status == "paid" and not self.payment_type:
            raise ValidationError({"payment_type": "To'lov holati `To'landi`ga o'tkazilganda, to'lov turini belgilash kerak"})
        return super().clean()


    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"



class OrderItem(models.Model):
    order = models.ForeignKey(verbose_name="Buyurtma", related_name="items", to=Order, on_delete=models.CASCADE)
    product_name = models.CharField("Mahsulot nomi", max_length=255)
    qty = models.IntegerField("Soni", default=0)
    price = models.IntegerField("Narxi", default=0)

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"