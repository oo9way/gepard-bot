# Generated by Django 4.2 on 2024-08-25 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_order_payment_status_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('paid', "To'langan"), ('unpaid', "To'lanmagan")], default='unpaid', max_length=16, verbose_name="To'lov holati"),
        ),
    ]