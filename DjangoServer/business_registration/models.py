import os
from django.db import models
import random
from django.db import models
from django.forms import ValidationError

class BusinessStatus(models.TextChoices):
    NEWLY_ESTABLISHED = 'NE', 'Mới thành lập'
    OPERATING = 'OP', 'Đang hoạt động'
    DISSOLVING = 'DI', 'Đang giải thể'
    BANKRUPT = 'BA', 'Đang phá sản'


class Business(models.Model):
    def validate_multiple_of_1000(value):
        if value % 1000 != 0:
            raise ValidationError(
                ('%(value)s is not a multiple of 1000'),
                params={'value': value},
            )
        
    def generate_unique_random_code():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'business_code.txt')
        with open(file_path, 'r+') as file:
            codes = file.readlines()
            if not codes:
                raise ValueError("No codes available")
            position = random.randint(0, len(codes) - 1)
            code = codes[position].strip()
            del codes[position]
            file.seek(0)
            file.truncate()
            file.writelines(codes)
        return code

    business_code = models.CharField(max_length=255, default=generate_unique_random_code, editable=False)  # Mã duy nhất cho mỗi doanh nghiệp
    company_name = models.CharField(max_length=255)  # Tên của công ty
    detail = models.TextField(null=True)  # Thông tin chi tiết về doanh nghiệp
    capital = models.BigIntegerField(validators=[validate_multiple_of_1000])  # Số vốn của doanh nghiệp
    status = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
        default=BusinessStatus.NEWLY_ESTABLISHED,
    )  # Trạng thái của doanh nghiệp
    legal_representative = models.ForeignKey('LegalRepresentative', on_delete=models.CASCADE)  # Người đại diện pháp luật của doanh nghiệp
    issued_date = models.DateField()  # Ngày cấp phép cho doanh nghiệp
    business_type = models.ForeignKey('BusinessType', on_delete=models.CASCADE) # Loại hình doanh nghiệp
    main_industry = models.ForeignKey('Industry', on_delete=models.CASCADE, related_name='+')  # Ngành nghề kinh doanh chính

class BusinessStatusChange(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    old_status = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
    )  # Trạng thái cũ của doanh nghiệp
    new_status = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
    )  # Trạng thái mới của doanh nghiệp
    change_date = models.DateField(auto_now_add=True)  # Ngày thay đổi trạng thái
    # changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Người thực hiện thay đổi trạng thái

class LegalRepresentative(models.Model):
    name = models.CharField(max_length=255)  # Tên của người đại diện pháp luật
    position = models.CharField(max_length=255)  # Chức vụ của người đại diện pháp luật

class Owner(models.Model):
    name = models.CharField(max_length=255)  # Tên của chủ sở hữu

class BusinessOwner(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Khóa ngoại đến model Owner

class BusinessType(models.Model):
    type_description = models.CharField(max_length=255) # Mô tả về loại hình doanh nghiệp

class BusinessTypeStatus(models.Model):
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)  # Khóa ngoại đến model BusinessType
    status = models.CharField(
        max_length=2,
        choices=BusinessStatus.choices,
    )  # Trạng thái doanh nghiệp

class BusinessProcessStep(models.Model):
    business_type_status = models.ForeignKey(BusinessTypeStatus, on_delete=models.CASCADE)  # Khóa ngoại đến model BusinessTypeStatus
    step_name = models.CharField(max_length=255)  # Tên của bước trong quy trình
    step_order = models.IntegerField()  # Thứ tự của bước trong quy trình
    step_description = models.TextField()  # Mô tả nội dung cho mỗi bước

class Industry(models.Model):
    activity_code = models.IntegerField()  # Mã của ngành nghề kinh doanh
    activity_name = models.CharField(max_length=255)  # Tên của ngành nghề kinh doanh

class BusinessIndustry(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)  # Khóa ngoại đến model Industry

class ActivityField(models.Model):
    field_code = models.IntegerField()  # Mã của lĩnh vực hoạt động
    field_name = models.CharField(max_length=255)  # Tên của lĩnh vực hoạt động

class BusinessActivityField(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    activity_field = models.ForeignKey(ActivityField, on_delete=models.CASCADE)  # Khóa ngoại đến model ActivityField

class Contacts(models.Model):
    phone = models.CharField(max_length=255) # Số điện thoại
    email = models.CharField(max_length=255)  # Địa chỉ email
    fax = models.CharField(max_length=255) # Số fax
    business = models.ForeignKey(Business, on_delete=models.CASCADE) # Khóa ngoại đến model Business

class Addresses(models.Model):
    detail = models.CharField(max_length=255) # Địa chỉ chi tiết
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE) # Khóa ngoại đến model Ward
    business = models.ForeignKey(Business, on_delete=models.CASCADE) # Khóa ngoại đến model Business

    def __str__(self):
        # provice / district / ward / detail
        province = self.ward.district.province.name
        district = self.ward.district.name
        ward = self.ward.name
        detail = self.detail
        return f'{detail}, {ward}, {district}, {province}'
    
class AdministrativeUnit(models.Model):
    full_name = models.CharField(max_length=255) # Tên đầy đủ
    full_name_en = models.CharField(max_length=255, blank=True) # Tên đầy đủ tiếng Anh
    short_name = models.CharField(max_length=255, blank=True) # Tên viết tắt
    short_name_en = models.CharField(max_length=255, blank=True) # Tên viết tắt tiếng Anh
    code_name = models.CharField(max_length=255, blank=True) # Tên mã
    code_name_en = models.CharField(max_length=255, blank=True) # Tên mã tiếng Anh

    def __str__(self):
        return self.full_name
    
class AdministrativeRegion(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    code_name = models.CharField(max_length=255, blank=True)
    code_name_en = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Province(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255) # Tên
    name_en = models.CharField(max_length=255, blank=True) # Tên tiếng Anh
    full_name = models.CharField(max_length=255, blank=True) # Tên đầy đủ
    full_name_en = models.CharField(max_length=255, blank=True) # Tên đầy đủ tiếng Anh
    code_name = models.CharField(max_length=255, blank=True) # Tên mã
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE) # Khóa ngoại đến model AdministrativeUnit
    administrative_region = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)  # Khóa ngoại đến model AdministrativeRegion

    def __str__(self):
        return self.name
    
class District(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255) # Tên
    name_en = models.CharField(max_length=255, blank=True) # Tên tiếng Anh
    full_name = models.CharField(max_length=255, blank=True) # Tên đầy đủ
    full_name_en = models.CharField(max_length=255, blank=True) # Tên đầy đủ tiếng Anh
    code_name = models.CharField(max_length=255, blank=True) # Tên mã
    province = models.ForeignKey(Province, on_delete=models.CASCADE) # Khóa ngoại đến model Province
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE) # Khóa ngoại đến model AdministrativeUnit

    def __str__(self):
        return self.name
    
class Ward(models.Model):
    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    full_name_en = models.CharField(max_length=255, blank=True)
    code_name = models.CharField(max_length=255, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
