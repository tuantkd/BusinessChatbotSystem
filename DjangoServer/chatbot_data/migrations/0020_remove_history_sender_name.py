# Generated by Django 4.2.9 on 2024-04-06 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_data', '0019_chatuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='sender_name',
        ),
    ]