# Generated by Django 4.2.6 on 2023-10-31 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionLuces', '0003_remove_sensores_ip_remove_sensores_last_signal_late_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aulas',
            name='last_signal_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 31, 19, 30, 10, 633744)),
        ),
        migrations.AlterField(
            model_name='registrosluces',
            name='hasta',
            field=models.DateTimeField(null=True),
        ),
    ]
