# Generated by Django 3.2.4 on 2022-08-30 00:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20220726_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationorder',
            name='released_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='creation_hour',
            field=models.TimeField(default=datetime.time(21, 1, 39, 216754), verbose_name='Hora da criação'),
        ),
        migrations.AlterField(
            model_name='medicationorder',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Liberado'), (2, 'Recusado')], default=0, verbose_name='Status'),
        ),
    ]
