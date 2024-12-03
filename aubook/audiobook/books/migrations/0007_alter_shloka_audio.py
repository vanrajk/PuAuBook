# Generated by Django 5.1 on 2024-08-30 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_alter_shloka_audio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shloka",
            name="audio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="books.audiofile",
            ),
        ),
    ]