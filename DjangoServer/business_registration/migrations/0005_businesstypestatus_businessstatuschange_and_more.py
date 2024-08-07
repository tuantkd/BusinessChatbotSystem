# Generated by Django 4.2.9 on 2024-02-19 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business_registration', '0004_addresses_district_addresses_province_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessTypeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản')], max_length=2)),
                ('business_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstype')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessStatusChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản')], max_length=2)),
                ('new_status', models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản')], max_length=2)),
                ('change_date', models.DateField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=255)),
                ('step_order', models.IntegerField()),
                ('step_description', models.TextField()),
                ('business_type_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstypestatus')),
            ],
        ),
    ]
