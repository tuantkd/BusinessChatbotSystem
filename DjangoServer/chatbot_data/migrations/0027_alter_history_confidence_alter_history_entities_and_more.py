# Generated by Django 4.2.9 on 2024-05-22 23:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_data', '0026_test_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='confidence',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='history',
            name='entities',
            field=models.TextField(blank=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='history',
            name='intent',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='history',
            name='intent_ranking',
            field=models.TextField(blank=True, default='[]'),
        ),
        migrations.AlterField(
            model_name='history',
            name='next_action',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='history',
            name='response',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='history',
            name='sender_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='history',
            name='slot_values',
            field=models.TextField(blank=True, default='{}'),
        ),
        migrations.AlterField(
            model_name='history',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='history',
            name='user_say',
            field=models.TextField(blank=True, default=''),
        ),
    ]