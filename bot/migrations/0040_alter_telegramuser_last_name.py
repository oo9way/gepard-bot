# Generated by Django 4.2 on 2024-09-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0039_telegramuser_address_telegramuser_contract_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='Фамилия'),
        ),
    ]