# Generated by Django 5.1 on 2024-08-30 09:59

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0004_rename_audio_file_shloka_audio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shloka",
            name="audio",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name=books.models.AudioFile
            ),
        ),
    ]
