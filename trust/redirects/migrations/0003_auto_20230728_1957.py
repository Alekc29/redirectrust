# Generated by Django 2.2.16 on 2023-07-28 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirects', '0002_auto_20230728_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='date_balance',
            field=models.DateField(blank=True, null=True, verbose_name='Дата проверки баланса'),
        ),
    ]
