# Generated by Django 4.2 on 2024-09-02 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_product_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Связаться с нами', 'verbose_name_plural': 'Связаться с нами'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Менеджер', 'verbose_name_plural': 'Менеджеры'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Заказать товар', 'verbose_name_plural': 'Заказать продукцию'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='telegramuser',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterField(
            model_name='category',
            name='cover',
            field=models.ImageField(upload_to='categories', verbose_name='Изображение категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('director', 'Директор'), ('accountant', 'Бухгалтер'), ('storekeeper', 'Заведующий складом')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='accountant_approve_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время утверждения бухгалтером'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время размещения заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='director_approve_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время утверждения директором'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Оплаченный'), ('unpaid', 'Неоплачиваемый')], default='unpaid', max_length=16, verbose_name='Статус платежа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('payme', 'Payme'), ('click', 'Click'), ('terminal', 'Терминал'), ('other', 'Другой')], max_length=16, null=True, verbose_name='Тип платежа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Новый'), ('approved_by_account', 'Аттестовано бухгалтером'), ('approved_by_director', 'Утверждено директором'), ('approved_by_storekeeper', 'Подтверждено кладовщиком')], default='pending', max_length=24, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='storekeeper_approve_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время одобрения кладовщика'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.telegramuser', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bot.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_name',
            field=models.CharField(max_length=255, verbose_name='Название продукта'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='qty',
            field=models.IntegerField(default=0, verbose_name='Число'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Число'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='bot.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cover',
            field=models.ImageField(upload_to='products', verbose_name='Изображение продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_top',
            field=models.BooleanField(default=False, verbose_name='Популярный продукт'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_usd',
            field=models.IntegerField(default=0, verbose_name='Цена (долл. США)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_uzs',
            field=models.IntegerField(default=0, verbose_name='Цена (сум)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название продукта'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='is_agent',
            field=models.BooleanField(default=False, verbose_name='Торговый представитель ?'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер телефона'),
        ),
    ]
