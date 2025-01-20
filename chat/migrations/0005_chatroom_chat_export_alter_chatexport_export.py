# Generated by Django 5.0.6 on 2025-01-20 15:52

import chat.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_rename_message_content_message_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="chat_export",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="chat_room",
                to="chat.chatexport",
            ),
        ),
        migrations.AlterField(
            model_name="chatexport",
            name="export",
            field=models.FileField(upload_to=chat.models.upload_user_path),
        ),
    ]
