# Generated by Django 4.2.9 on 2024-04-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_data', '0017_rename_sender_history_sender_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='sender_name',
            field=models.TextField(default=str),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='slot_values',
            field=models.TextField(blank=True, null=True),
        ),
    ]
