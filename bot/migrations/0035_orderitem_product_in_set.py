# Generated by Django 4.2 on 2024-09-16 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0034_orderitem_set_amount_telegramuser_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product_in_set',
            field=models.FloatField(default=0, verbose_name='Количество в Набор'),
        ),
    ]