# Generated by Django 4.2 on 2023-04-27 06:31

import account.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_alter_account_options_account_date_joined_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="account",
            managers=[
                ("objects", account.models.UserManager()),
            ],
        ),
    ]
