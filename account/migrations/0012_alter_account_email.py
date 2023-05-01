# Generated by Django 4.2 on 2023-05-01 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0011_alter_account_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
    ]
