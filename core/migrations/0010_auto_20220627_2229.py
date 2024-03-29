# Generated by Django 3.2.4 on 2022-06-28 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220620_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='creation_hour',
            field=models.TimeField(default=datetime.time(22, 29, 34, 673204), verbose_name='Hora da criação'),
        ),
        migrations.AlterField(
            model_name='attendancequeue',
            name='attendances',
            field=models.JSONField(blank=True),
        ),
    ]
