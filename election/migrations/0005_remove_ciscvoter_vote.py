# Generated by Django 3.0.5 on 2020-05-28 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0004_auto_20200527_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciscvoter',
            name='vote',
        ),
    ]