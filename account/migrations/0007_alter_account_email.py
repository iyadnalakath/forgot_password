# Generated by Django 4.2 on 2023-05-01 00:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_passwordrest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="email"),
        ),
    ]
