# Generated by Django 5.1 on 2024-08-30 06:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_shloka_shloka_number_alter_audiofile_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shloka",
            old_name="audio_file",
            new_name="audio",
        ),
    ]
