# Generated by Django 5.0.2 on 2024-03-10 02:45

import business_registration.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_registration', '0010_business_issue_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityfield',
            options={'verbose_name': 'Activity Field', 'verbose_name_plural': 'Activity Fields'},
        ),
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='administrativeregion',
            options={'verbose_name': 'Administrative Region', 'verbose_name_plural': 'Administrative Regions'},
        ),
        migrations.AlterModelOptions(
            name='administrativeunit',
            options={'verbose_name': 'Administrative Unit', 'verbose_name_plural': 'Administrative Units'},
        ),
        migrations.AlterModelOptions(
            name='business',
            options={'verbose_name': 'Business', 'verbose_name_plural': 'Businesses'},
        ),
        migrations.AlterModelOptions(
            name='businessactivityfield',
            options={'verbose_name': 'Business Activity Field', 'verbose_name_plural': 'Business Activity Fields'},
        ),
        migrations.AlterModelOptions(
            name='businessaddress',
            options={'verbose_name': 'Business Address', 'verbose_name_plural': 'Business Addresses'},
        ),
        migrations.AlterModelOptions(
            name='businessindustry',
            options={'verbose_name': 'Business Industry', 'verbose_name_plural': 'Business Industries'},
        ),
        migrations.AlterModelOptions(
            name='businessowner',
            options={'verbose_name': 'Business Owner', 'verbose_name_plural': 'Business Owners'},
        ),
        migrations.AlterModelOptions(
            name='businessprocessstep',
            options={'verbose_name': 'Business Process Step', 'verbose_name_plural': 'Business Process Steps'},
        ),
        migrations.AlterModelOptions(
            name='businessstatuschange',
            options={'verbose_name': 'Business Status Change', 'verbose_name_plural': 'Business Status Changes'},
        ),
        migrations.AlterModelOptions(
            name='businesstype',
            options={'verbose_name': 'Business Type', 'verbose_name_plural': 'Business Types'},
        ),
        migrations.AlterModelOptions(
            name='businesstypestatus',
            options={'verbose_name': 'Business Type Status', 'verbose_name_plural': 'Business Type Statuses'},
        ),
        migrations.AlterModelOptions(
            name='contacts',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'District', 'verbose_name_plural': 'Districts'},
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name': 'Industry', 'verbose_name_plural': 'Industries'},
        ),
        migrations.AlterModelOptions(
            name='legalrepresentative',
            options={'verbose_name': 'Legal Representative', 'verbose_name_plural': 'Legal Representatives'},
        ),
        migrations.AlterModelOptions(
            name='owner',
            options={'verbose_name': 'Owner', 'verbose_name_plural': 'Owners'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'verbose_name': 'Province', 'verbose_name_plural': 'Provinces'},
        ),
        migrations.AlterModelOptions(
            name='ward',
            options={'verbose_name': 'Ward', 'verbose_name_plural': 'Wards'},
        ),
        migrations.RemoveField(
            model_name='business',
            name='issue_date',
        ),
        migrations.AlterField(
            model_name='activityfield',
            name='field_code',
            field=models.IntegerField(verbose_name='Field Code'),
        ),
        migrations.AlterField(
            model_name='activityfield',
            name='field_name',
            field=models.CharField(max_length=255, verbose_name='Field Name'),
        ),
        migrations.AlterField(
            model_name='address',
            name='detail',
            field=models.CharField(max_length=255, verbose_name='Detail'),
        ),
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.district', verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.province', verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='address',
            name='ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.ward', verbose_name='Ward'),
        ),
        migrations.AlterField(
            model_name='administrativeregion',
            name='code_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name'),
        ),
        migrations.AlterField(
            model_name='administrativeregion',
            name='code_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name (English)'),
        ),
        migrations.AlterField(
            model_name='administrativeregion',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='administrativeregion',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name (English)'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='code_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='code_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name (English)'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name (English)'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='short_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Short Name'),
        ),
        migrations.AlterField(
            model_name='administrativeunit',
            name='short_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Short Name (English)'),
        ),
        migrations.AlterField(
            model_name='business',
            name='business_code',
            field=models.CharField(default=business_registration.models.Business.generate_unique_random_code, editable=False, max_length=255, verbose_name='Business Code'),
        ),
        migrations.AlterField(
            model_name='business',
            name='business_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstype', verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='business',
            name='capital',
            field=models.BigIntegerField(validators=[business_registration.models.Business.validate_multiple_of_1000], verbose_name='Capital'),
        ),
        migrations.AlterField(
            model_name='business',
            name='company_name',
            field=models.CharField(max_length=255, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='business',
            name='detail',
            field=models.TextField(blank=True, null=True, verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='business',
            name='headquarters_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='business_registration.address', verbose_name='Headquarters Address'),
        ),
        migrations.AlterField(
            model_name='business',
            name='issued_date',
            field=models.DateField(verbose_name='Issued Date'),
        ),
        migrations.AlterField(
            model_name='business',
            name='legal_representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_registration.legalrepresentative', verbose_name='Legal Representative'),
        ),
        migrations.AlterField(
            model_name='business',
            name='main_industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='business_registration.industry', verbose_name='Main Industry'),
        ),
        migrations.AlterField(
            model_name='business',
            name='status',
            field=models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản'), ('NR', 'Đăng ký mới'), ('CR', 'Thay đổi đăng ký'), ('CN', 'Thông báo thay đổi'), ('TS', 'Tạm ngừng'), ('OC', 'Trường hợp khác'), ('LD', 'Văn bản pháp luật'), ('TO', 'Chấm dứt hoạt động'), ('BL', 'Thay đổi địa điểm kinh doanh'), ('PE', 'Doanh nghiệp tư nhân'), ('LP', 'Công ty TNHH 1 TV'), ('JS', 'Công ty Cổ phần'), ('MG', 'Hợp nhất doanh nghiệp'), ('BS', 'Chia doanh nghiệp'), ('BC', 'Chuyển đổi loại hình doanh nghiệp'), ('NE2', 'Thành lập mới'), ('CR2', 'Đăng ký thay đổi'), ('NC', 'Thông báo thay đổi'), ('TS2', 'Tạm ngừng'), ('DI2', 'Giải thể'), ('OC2', 'Trường hợp khác'), ('LD2', 'Văn bản pháp luật'), ('TO2', 'Chấm dứt hoạt động'), ('BL2', 'Địa điểm kinh doanh'), ('TO3', 'Chấm dứt hoạt động'), ('TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'), ('TO4', 'Chấm dứt hoạt động'), ('BS2', 'Chia doanh nghiệp'), ('BS3', 'Tách doanh nghiệp'), ('MG2', 'Hợp nhất doanh nghiệp'), ('BC2', 'Chuyển đổi loại hình doanh nghiệp'), ('BL3', 'Địa điểm kinh doanh'), ('OC3', 'Trường hợp khác'), ('LD3', 'Văn bản pháp luật'), ('PE2', 'Doanh nghiệp tư nhân'), ('LP2', 'Công ty TNHH 2 TV'), ('JS2', 'Công ty Cổ phần')], default='NE', max_length=5, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='businessactivityfield',
            name='activity_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.activityfield', verbose_name='Activity Field'),
        ),
        migrations.AlterField(
            model_name='businessactivityfield',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business', verbose_name='Business'),
        ),
        migrations.AlterField(
            model_name='businessaddress',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.address', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='businessaddress',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business', verbose_name='Business'),
        ),
        migrations.AlterField(
            model_name='businessindustry',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business', verbose_name='Business'),
        ),
        migrations.AlterField(
            model_name='businessindustry',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.industry', verbose_name='Industry'),
        ),
        migrations.AlterField(
            model_name='businessowner',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business', verbose_name='Business'),
        ),
        migrations.AlterField(
            model_name='businessowner',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.owner', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='businessprocessstep',
            name='business_type_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstypestatus', verbose_name='Business Type Status'),
        ),
        migrations.AlterField(
            model_name='businessprocessstep',
            name='step_description',
            field=models.TextField(verbose_name='Step Description'),
        ),
        migrations.AlterField(
            model_name='businessprocessstep',
            name='step_name',
            field=models.CharField(max_length=255, verbose_name='Step Name'),
        ),
        migrations.AlterField(
            model_name='businessprocessstep',
            name='step_order',
            field=models.IntegerField(verbose_name='Step Order'),
        ),
        migrations.AlterField(
            model_name='businessstatuschange',
            name='new_status',
            field=models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản'), ('NR', 'Đăng ký mới'), ('CR', 'Thay đổi đăng ký'), ('CN', 'Thông báo thay đổi'), ('TS', 'Tạm ngừng'), ('OC', 'Trường hợp khác'), ('LD', 'Văn bản pháp luật'), ('TO', 'Chấm dứt hoạt động'), ('BL', 'Thay đổi địa điểm kinh doanh'), ('PE', 'Doanh nghiệp tư nhân'), ('LP', 'Công ty TNHH 1 TV'), ('JS', 'Công ty Cổ phần'), ('MG', 'Hợp nhất doanh nghiệp'), ('BS', 'Chia doanh nghiệp'), ('BC', 'Chuyển đổi loại hình doanh nghiệp'), ('NE2', 'Thành lập mới'), ('CR2', 'Đăng ký thay đổi'), ('NC', 'Thông báo thay đổi'), ('TS2', 'Tạm ngừng'), ('DI2', 'Giải thể'), ('OC2', 'Trường hợp khác'), ('LD2', 'Văn bản pháp luật'), ('TO2', 'Chấm dứt hoạt động'), ('BL2', 'Địa điểm kinh doanh'), ('TO3', 'Chấm dứt hoạt động'), ('TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'), ('TO4', 'Chấm dứt hoạt động'), ('BS2', 'Chia doanh nghiệp'), ('BS3', 'Tách doanh nghiệp'), ('MG2', 'Hợp nhất doanh nghiệp'), ('BC2', 'Chuyển đổi loại hình doanh nghiệp'), ('BL3', 'Địa điểm kinh doanh'), ('OC3', 'Trường hợp khác'), ('LD3', 'Văn bản pháp luật'), ('PE2', 'Doanh nghiệp tư nhân'), ('LP2', 'Công ty TNHH 2 TV'), ('JS2', 'Công ty Cổ phần')], max_length=5, verbose_name='New Status'),
        ),
        migrations.AlterField(
            model_name='businessstatuschange',
            name='old_status',
            field=models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản'), ('NR', 'Đăng ký mới'), ('CR', 'Thay đổi đăng ký'), ('CN', 'Thông báo thay đổi'), ('TS', 'Tạm ngừng'), ('OC', 'Trường hợp khác'), ('LD', 'Văn bản pháp luật'), ('TO', 'Chấm dứt hoạt động'), ('BL', 'Thay đổi địa điểm kinh doanh'), ('PE', 'Doanh nghiệp tư nhân'), ('LP', 'Công ty TNHH 1 TV'), ('JS', 'Công ty Cổ phần'), ('MG', 'Hợp nhất doanh nghiệp'), ('BS', 'Chia doanh nghiệp'), ('BC', 'Chuyển đổi loại hình doanh nghiệp'), ('NE2', 'Thành lập mới'), ('CR2', 'Đăng ký thay đổi'), ('NC', 'Thông báo thay đổi'), ('TS2', 'Tạm ngừng'), ('DI2', 'Giải thể'), ('OC2', 'Trường hợp khác'), ('LD2', 'Văn bản pháp luật'), ('TO2', 'Chấm dứt hoạt động'), ('BL2', 'Địa điểm kinh doanh'), ('TO3', 'Chấm dứt hoạt động'), ('TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'), ('TO4', 'Chấm dứt hoạt động'), ('BS2', 'Chia doanh nghiệp'), ('BS3', 'Tách doanh nghiệp'), ('MG2', 'Hợp nhất doanh nghiệp'), ('BC2', 'Chuyển đổi loại hình doanh nghiệp'), ('BL3', 'Địa điểm kinh doanh'), ('OC3', 'Trường hợp khác'), ('LD3', 'Văn bản pháp luật'), ('PE2', 'Doanh nghiệp tư nhân'), ('LP2', 'Công ty TNHH 2 TV'), ('JS2', 'Công ty Cổ phần')], max_length=5, verbose_name='Old Status'),
        ),
        migrations.AlterField(
            model_name='businesstype',
            name='type_description',
            field=models.CharField(max_length=255, verbose_name='Type Description'),
        ),
        migrations.AlterField(
            model_name='businesstypestatus',
            name='business_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.businesstype', verbose_name='Business Type'),
        ),
        migrations.AlterField(
            model_name='businesstypestatus',
            name='status',
            field=models.CharField(choices=[('NE', 'Mới thành lập'), ('OP', 'Đang hoạt động'), ('DI', 'Đang giải thể'), ('BA', 'Đang phá sản'), ('NR', 'Đăng ký mới'), ('CR', 'Thay đổi đăng ký'), ('CN', 'Thông báo thay đổi'), ('TS', 'Tạm ngừng'), ('OC', 'Trường hợp khác'), ('LD', 'Văn bản pháp luật'), ('TO', 'Chấm dứt hoạt động'), ('BL', 'Thay đổi địa điểm kinh doanh'), ('PE', 'Doanh nghiệp tư nhân'), ('LP', 'Công ty TNHH 1 TV'), ('JS', 'Công ty Cổ phần'), ('MG', 'Hợp nhất doanh nghiệp'), ('BS', 'Chia doanh nghiệp'), ('BC', 'Chuyển đổi loại hình doanh nghiệp'), ('NE2', 'Thành lập mới'), ('CR2', 'Đăng ký thay đổi'), ('NC', 'Thông báo thay đổi'), ('TS2', 'Tạm ngừng'), ('DI2', 'Giải thể'), ('OC2', 'Trường hợp khác'), ('LD2', 'Văn bản pháp luật'), ('TO2', 'Chấm dứt hoạt động'), ('BL2', 'Địa điểm kinh doanh'), ('TO3', 'Chấm dứt hoạt động'), ('TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'), ('TO4', 'Chấm dứt hoạt động'), ('BS2', 'Chia doanh nghiệp'), ('BS3', 'Tách doanh nghiệp'), ('MG2', 'Hợp nhất doanh nghiệp'), ('BC2', 'Chuyển đổi loại hình doanh nghiệp'), ('BL3', 'Địa điểm kinh doanh'), ('OC3', 'Trường hợp khác'), ('LD3', 'Văn bản pháp luật'), ('PE2', 'Doanh nghiệp tư nhân'), ('LP2', 'Công ty TNHH 2 TV'), ('JS2', 'Công ty Cổ phần')], max_length=5, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.business', verbose_name='Business'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.CharField(max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='fax',
            field=models.CharField(max_length=255, verbose_name='Fax'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='district',
            name='administrative_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit', verbose_name='Administrative Unit'),
        ),
        migrations.AlterField(
            model_name='district',
            name='code_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name'),
        ),
        migrations.AlterField(
            model_name='district',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='district',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name (English)'),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='district',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name (English)'),
        ),
        migrations.AlterField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.province', verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='industry',
            name='activity_code',
            field=models.IntegerField(verbose_name='Activity Code'),
        ),
        migrations.AlterField(
            model_name='industry',
            name='activity_name',
            field=models.CharField(max_length=255, verbose_name='Activity Name'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='contact_address',
            field=models.TextField(verbose_name='Contact Address'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='dob',
            field=models.DateField(verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='ethnicity',
            field=models.CharField(max_length=50, verbose_name='Ethnicity'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='gender',
            field=models.CharField(max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='id_issuance_date',
            field=models.DateField(verbose_name='ID Issuance Date'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='id_issuance_place',
            field=models.CharField(max_length=255, verbose_name='ID Issuance Place'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='id_number',
            field=models.CharField(max_length=20, verbose_name='ID Number'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='id_type',
            field=models.CharField(max_length=255, verbose_name='ID Type'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='nationality',
            field=models.CharField(max_length=50, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='position',
            field=models.CharField(max_length=255, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='legalrepresentative',
            name='residence_address',
            field=models.TextField(verbose_name='Residence Address'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='contact_address',
            field=models.TextField(verbose_name='Contact Address'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='dob',
            field=models.DateField(verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='ethnicity',
            field=models.CharField(max_length=50, verbose_name='Ethnicity'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='gender',
            field=models.CharField(max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='id_issuance_date',
            field=models.DateField(verbose_name='ID Issuance Date'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='id_issuance_place',
            field=models.CharField(max_length=255, verbose_name='ID Issuance Place'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='id_number',
            field=models.CharField(max_length=20, verbose_name='ID Number'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='id_type',
            field=models.CharField(max_length=100, verbose_name='ID Type'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='nationality',
            field=models.CharField(max_length=50, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='residence_address',
            field=models.TextField(verbose_name='Residence Address'),
        ),
        migrations.AlterField(
            model_name='province',
            name='administrative_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeregion', verbose_name='Administrative Region'),
        ),
        migrations.AlterField(
            model_name='province',
            name='administrative_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit', verbose_name='Administrative Unit'),
        ),
        migrations.AlterField(
            model_name='province',
            name='code_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name'),
        ),
        migrations.AlterField(
            model_name='province',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='province',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name (English)'),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='province',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name (English)'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='administrative_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.administrativeunit', verbose_name='Administrative Unit'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='code_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Code Name'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business_registration.district', verbose_name='District'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name (English)'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name (English)'),
        ),
    ]
