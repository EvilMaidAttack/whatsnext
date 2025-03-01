# Generated by Django 5.0.6 on 2025-01-19 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_message_chat_room"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="message_content",
            new_name="content",
        ),
        migrations.RenameField(
            model_name="message",
            old_name="sent_at",
            new_name="timestamp",
        ),
        migrations.CreateModel(
            name="ChatExport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("export", models.FileField(upload_to="chat_exports/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_exports",
                        to="chat.profile",
                    ),
                ),
            ],
        ),
    ]
