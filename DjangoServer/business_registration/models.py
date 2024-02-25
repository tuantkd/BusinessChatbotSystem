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
    NEWLY_REGISTERED = 'NR', 'Đăng ký mới'
    CHANGE_REGISTERED = 'CR', 'Thay đổi đăng ký'
    CHANGE_NOTIFICATION = 'CN', 'Thông báo thay đổi'
    TEMPORARILY_SUSPENDED = 'TS', 'Tạm ngừng'
    OTHER_CASES = 'OC', 'Trường hợp khác'
    LEGAL_DOCUMENT = 'LD', 'Văn bản pháp luật'
    TERMINATION_OF_OPERATION = 'TO', 'Chấm dứt hoạt động'
    BUSINESS_LOCATION_CHANGE = 'BL', 'Thay đổi địa điểm kinh doanh'
    PRIVATE_ENTERPRISE = 'PE', 'Doanh nghiệp tư nhân'
    LIMITED_PARTNERSHIP = 'LP', 'Công ty TNHH 1 TV'
    JOINT_STOCK_COMPANY = 'JS', 'Công ty Cổ phần'
    MERGER = 'MG', 'Hợp nhất doanh nghiệp'
    BUSINESS_SPLIT = 'BS', 'Chia doanh nghiệp'
    BUSINESS_CONVERSION = 'BC', 'Chuyển đổi loại hình doanh nghiệp'
    NEW_ESTABLISHMENT = 'NE2', 'Thành lập mới'
    CHANGE_REGISTRATION = 'CR2', 'Đăng ký thay đổi'
    NOTIFICATION_OF_CHANGE = 'NC', 'Thông báo thay đổi'
    TEMPORARY_SUSPENSION = 'TS2', 'Tạm ngừng'
    DISSOLUTION = 'DI2', 'Giải thể'
    OTHER_CASES_2 = 'OC2', 'Trường hợp khác'
    LEGAL_DOCUMENT_2 = 'LD2', 'Văn bản pháp luật'
    TERMINATION_OF_OPERATION_2 = 'TO2', 'Chấm dứt hoạt động'
    BUSINESS_LOCATION_CHANGE_2 = 'BL2', 'Địa điểm kinh doanh'
    TERMINATION_OF_OPERATION_3 = 'TO3', 'Chấm dứt hoạt động'
    TEMPORARY_SUSPENSION_2 = 'TS3', 'Tạm ngừng kinh doanh - tiếp tục kinh doanh trước thời hạn'
    TERMINATION_OF_OPERATION_4 = 'TO4', 'Chấm dứt hoạt động'
    BUSINESS_SPLIT_2 = 'BS2', 'Chia doanh nghiệp'
    BUSINESS_SPLIT_3 = 'BS3', 'Tách doanh nghiệp'
    MERGER_2 = 'MG2', 'Hợp nhất doanh nghiệp'
    BUSINESS_CONVERSION_2 = 'BC2', 'Chuyển đổi loại hình doanh nghiệp'
    BUSINESS_LOCATION_CHANGE_3 = 'BL3', 'Địa điểm kinh doanh'
    OTHER_CASES_3 = 'OC3', 'Trường hợp khác'
    LEGAL_DOCUMENT_3 = 'LD3', 'Văn bản pháp luật'
    PRIVATE_ENTERPRISE_2 = 'PE2', 'Doanh nghiệp tư nhân'
    LIMITED_PARTNERSHIP_2 = 'LP2', 'Công ty TNHH 2 TV'
    JOINT_STOCK_COMPANY_2 = 'JS2', 'Công ty Cổ phần'

    

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
        max_length=5,
        choices=BusinessStatus.choices,
        default=BusinessStatus.NEWLY_ESTABLISHED,
    )  # Trạng thái của doanh nghiệp
    legal_representative = models.ForeignKey('LegalRepresentative', on_delete=models.CASCADE,  null=True, blank=True)  # Người đại diện pháp luật của doanh nghiệp
    issued_date = models.DateField()  # Ngày cấp phép cho doanh nghiệp
    business_type = models.ForeignKey('BusinessType', on_delete=models.CASCADE) # Loại hình doanh nghiệp
    main_industry = models.ForeignKey('Industry', on_delete=models.CASCADE, related_name='+')  # Ngành nghề kinh doanh chính
    headquarters_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='+')  # Địa chỉ trụ sở chính
    issue_date = models.DateField(null=True, blank=True)
    
class BusinessStatusChange(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    old_status = models.CharField(
        max_length=5,
        choices=BusinessStatus.choices,
    )  # Trạng thái cũ của doanh nghiệp
    new_status = models.CharField(
        max_length=5,
        choices=BusinessStatus.choices,
    )  # Trạng thái mới của doanh nghiệp
    change_date = models.DateField(auto_now_add=True)  # Ngày thay đổi trạng thái
    # changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Người thực hiện thay đổi trạng thái

class LegalRepresentative(models.Model):
    name = models.CharField(max_length=255)  # Họ và tên
    gender = models.CharField(max_length=10)  # Giới tính
    position = models.CharField(max_length=255)  # Chức danh
    dob = models.DateField()  # Sinh ngày (Date of Birth)
    ethnicity = models.CharField(max_length=50)  # Dân tộc
    nationality = models.CharField(max_length=50)  # Quốc tịch
    id_type = models.CharField(max_length=255)  # Loại giấy tờ pháp lý (The can cuoc cong dan)
    id_number = models.CharField(max_length=20)  # Số giấy tờ pháp lý
    id_issuance_date = models.DateField()  # Ngày cấp
    id_issuance_place = models.CharField(max_length=255)  # Nơi cấp
    residence_address = models.TextField()  # Địa chỉ thường trú
    contact_address = models.TextField()  # Địa chỉ liên lạc

    def __str__(self):
        return self.name

class Owner(models.Model):
    name = models.CharField(max_length=255)  # Họ và tên
    gender = models.CharField(max_length=10)  # Giới tính
    dob = models.DateField()  # Ngày, tháng, năm sinh
    ethnicity = models.CharField(max_length=50)  # Dân tộc
    nationality = models.CharField(max_length=50)  # Quốc tịch
    id_type = models.CharField(max_length=100)  # Loại giấy tờ pháp lý
    id_number = models.CharField(max_length=20)  # Số giấy tờ pháp lý
    id_issuance_date = models.DateField()  # Ngày cấp
    id_issuance_place = models.CharField(max_length=255)  # Nơi cấp
    residence_address = models.TextField()  # Địa chỉ thường trú
    contact_address = models.TextField()  # Địa chỉ liên lạc

    def __str__(self):
        return self.name

class BusinessOwner(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Khóa ngoại đến model Owner

class BusinessType(models.Model):
    type_description = models.CharField(max_length=255) # Mô tả về loại hình doanh nghiệp

class BusinessTypeStatus(models.Model):
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)  # Khóa ngoại đến model BusinessType
    status = models.CharField(
        max_length=5,
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

class Address(models.Model):
    detail = models.CharField(max_length=255) # Địa chỉ chi tiết
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE) # Khóa ngoại đến model Ward

class BusinessAddress(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE) # Khóa ngoại đến model Business
    address = models.ForeignKey(Address, on_delete=models.CASCADE) # Khóa ngoại đến model Address
    
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
