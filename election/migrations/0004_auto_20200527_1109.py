# Generated by Django 3.0.5 on 2020-05-27 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0003_election_campus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='election',
            old_name='campus',
            new_name='voter_campus',
        ),
        migrations.RemoveField(
            model_name='election',
            name='voter_type',
        ),
    ]