# Generated by Django 3.2.9 on 2022-01-03 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_recepient_message_recipient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created']},
        ),
    ]