# Generated by Django 5.1 on 2024-08-30 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0005_alter_shloka_audio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shloka",
            name="audio",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="books.audiofile",
            ),
        ),
    ]