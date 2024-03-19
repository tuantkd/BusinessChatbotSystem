# Generated by Django 4.2.9 on 2024-03-12 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactive_chatbot', '0002_action_entity_expression_nlulog_settings_synonym_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='expression',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='expressionparameter',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='expressionparameter',
            name='expression',
        ),
        migrations.RemoveField(
            model_name='expressionparameter',
            name='intent',
        ),
        migrations.RemoveField(
            model_name='intent',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='modelmodel',
            name='bot',
        ),
        migrations.DeleteModel(
            name='NluLog',
        ),
        migrations.RemoveField(
            model_name='regex',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='response',
            name='action',
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
        migrations.RemoveField(
            model_name='story',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='synonym',
            name='bot',
        ),
        migrations.RemoveField(
            model_name='synonymvariant',
            name='synonym',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Entity',
        ),
        migrations.DeleteModel(
            name='Expression',
        ),
        migrations.DeleteModel(
            name='ExpressionParameter',
        ),
        migrations.DeleteModel(
            name='Intent',
        ),
        migrations.DeleteModel(
            name='ModelModel',
        ),
        migrations.DeleteModel(
            name='Regex',
        ),
        migrations.DeleteModel(
            name='Response',
        ),
        migrations.DeleteModel(
            name='Story',
        ),
        migrations.DeleteModel(
            name='Synonym',
        ),
        migrations.DeleteModel(
            name='SynonymVariant',
        ),
    ]
