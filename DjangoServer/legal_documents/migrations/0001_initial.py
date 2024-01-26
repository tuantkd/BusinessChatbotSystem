# Generated by Django 4.2.9 on 2024-01-26 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circulars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circular_number', models.CharField(max_length=255)),
                ('issued_date', models.DateField()),
                ('circular_name', models.TextField()),
                ('circular_link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Decisions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision_number', models.CharField(max_length=255)),
                ('issued_date', models.DateField()),
                ('decision_name', models.TextField()),
                ('decision_link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Decrees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decree_number', models.CharField(max_length=255)),
                ('issued_date', models.DateField()),
                ('decree_name', models.TextField()),
                ('decree_link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Laws',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('law_number', models.CharField(max_length=255)),
                ('issued_date', models.DateField()),
                ('law_name', models.TextField()),
                ('law_link', models.CharField(max_length=255)),
            ],
        ),
    ]