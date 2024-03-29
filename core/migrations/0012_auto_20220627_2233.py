# Generated by Django 3.2.4 on 2022-06-28 01:33

import datetime
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20220627_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='creation_hour',
            field=models.TimeField(default=datetime.time(22, 33, 20, 737955), verbose_name='Hora da criação'),
        ),
        migrations.AlterField(
            model_name='attendancequeue',
            name='attendances',
            field=jsonfield.fields.JSONField(blank=True, default=[]),
        ),
    ]
