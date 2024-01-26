# Generated by Django 4.2.9 on 2024-01-26 09:35

import business_registration.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_code', models.IntegerField()),
                ('field_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrativeRegion',
            fields=[
                ('code', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_en', models.CharField(blank=True, max_length=255)),
                ('code_name', models.CharField(blank=True, max_length=255)),
                ('code_name_en', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AdministrativeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('full_name_en', models.CharField(blank=True, max_length=255)),
                ('short_name', models.CharField(blank=True, max_length=255)),
                ('short_name_en', models.CharField(blank=True, max_length=255)),
                ('code_name', models.CharField(blank=True, max_length=255)),
                ('code_name_en', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_code', models.CharField(default=business_registration.models.Business.generate_unique_random_code, editable=False, max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('detail', models.CharField(max_length=255)),
                ('capital', models.BigIntegerField()),
                ('status', models.CharField(max_length=255)),
                ('issued_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('code', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_en', models.CharField(blank=True, max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('full_name_en', models.CharField(blank=True, max_length=255)),
                ('code_name', models.CharField(blank=True, max_length=255)),
                ('administrative_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit')),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_code', models.IntegerField()),
                ('activity_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LegalRepresentative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('code', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_en', models.CharField(blank=True, max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('full_name_en', models.CharField(blank=True, max_length=255)),
                ('code_name', models.CharField(blank=True, max_length=255)),
                ('administrative_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.district')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('code', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_en', models.CharField(blank=True, max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('full_name_en', models.CharField(blank=True, max_length=255)),
                ('code_name', models.CharField(blank=True, max_length=255)),
                ('administrative_region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeregion')),
                ('administrative_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.province'),
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('fax', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.owner')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.industry')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessActivityField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.activityfield')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
            ],
        ),
        migrations.AddField(
            model_name='business',
            name='business_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstype'),
        ),
        migrations.AddField(
            model_name='business',
            name='legal_representative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.legalrepresentative'),
        ),
        migrations.AddField(
            model_name='business',
            name='main_industry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='business_registration.industry'),
        ),
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.ward')),
            ],
        ),
    ]