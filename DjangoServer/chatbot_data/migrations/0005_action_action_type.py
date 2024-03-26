# Generated by Django 4.2.9 on 2024-03-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_data', '0004_alter_entity_bot_alter_expression_intent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='action_type',
            field=models.CharField(choices=[('utter', 'UTTER'), ('action', 'ACTION'), ('form', 'FORM'), ('slot_set', 'SLOT_SET')], default='utter', max_length=10),
        ),
    ]
