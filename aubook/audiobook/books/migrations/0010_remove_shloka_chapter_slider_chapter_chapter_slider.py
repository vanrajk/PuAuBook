# Generated by Django 4.2.14 on 2024-10-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0009_book_book_slider_shloka_chapter_slider"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shloka",
            name="chapter_slider",
        ),
        migrations.AddField(
            model_name="chapter",
            name="chapter_slider",
            field=models.ImageField(blank=True, null=True, upload_to="chapter_slider/"),
        ),
    ]
