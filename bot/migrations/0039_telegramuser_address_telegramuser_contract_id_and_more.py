# Generated by Django 4.2 on 2024-09-25 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0038_alter_product_price_usd_a_alter_product_price_usd_b_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='contract_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер договор'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Названия клиента'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
    ]