# Generated by Django 3.0.5 on 2020-05-05 01:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0008_auto_20200505_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='majorposition',
            name='date_candidacy',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
