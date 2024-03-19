# Generated by Django 4.2.9 on 2024-03-12 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatbot_data', '0002_remove_domain_menu_delete_history_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_name', models.TextField()),
                ('bot_config', models.TextField()),
                ('output_folder', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_name', models.TextField()),
                ('slot_data_type', models.TextField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='Expression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NluLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.TextField()),
                ('query', models.TextField()),
                ('event_type', models.TextField()),
                ('event_data', models.TextField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_name', models.TextField(unique=True)),
                ('setting_value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonym_reference', models.TextField()),
                ('regex_pattern', models.TextField(blank=True, null=True)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='SynonymVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonym_value', models.TextField()),
                ('synonym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.synonym')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_name', models.TextField()),
                ('story', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField()),
                ('response_type', models.TextField()),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.action')),
            ],
        ),
        migrations.CreateModel(
            name='Regex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex_name', models.TextField()),
                ('regex_pattern', models.TextField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='ModelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('comment', models.TextField()),
                ('local_path', models.TextField()),
                ('server_path', models.TextField()),
                ('server_response', models.TextField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='Intent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent_name', models.TextField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.CreateModel(
            name='ExpressionParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_start', models.IntegerField()),
                ('parameter_end', models.IntegerField()),
                ('parameter_value', models.TextField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.entity')),
                ('expression', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.expression')),
                ('intent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.intent')),
            ],
        ),
        migrations.AddField(
            model_name='expression',
            name='intent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.intent'),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.TextField(blank=True, null=True)),
                ('conversation', models.TextField()),
                ('story', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField()),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='bot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot_data.bot'),
        ),
    ]
