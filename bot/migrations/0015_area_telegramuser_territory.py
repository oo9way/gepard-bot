# Generated by Django 4.2 on 2024-09-02 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_telegramuser_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Территория',
                'verbose_name_plural': 'Территории',
            },
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='territory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.area', verbose_name='Территория'),
        ),
    ]
