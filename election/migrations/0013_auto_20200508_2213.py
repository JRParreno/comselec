# Generated by Django 3.0.5 on 2020-05-08 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0012_ciscvoter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciscvoter',
            name='vote',
            field=models.BooleanField(default=False),
        ),
    ]