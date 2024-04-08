import os
from django.db import models
import random
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

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

    def get_business_status_value_by_fullname(fullname):
        for value, full_name in BusinessStatus.choices:
            if full_name.lower() == fullname.lower():
                return value
        return None

class Business(models.Model):
    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Businesses")

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

    business_code = models.CharField(_("Business Code"), max_length=255, default=generate_unique_random_code, editable=False)
    company_name = models.CharField(_("Company Name"), max_length=255)
    longitude = models.CharField(_("Longitude"), max_length=20)
    latitude = models.CharField(_("Latitude"), max_length=20)
    address = models.CharField(_("Address"), max_length=255)
    company_name = models.CharField(_("Company Name"), max_length=255)
    detail = models.TextField(_("Details"), blank=True)
    capital = models.BigIntegerField(_("Capital"), validators=[validate_multiple_of_1000])
    status = models.CharField(
        _("Status"),
        max_length=5,
        choices=BusinessStatus.choices,
        default=BusinessStatus.NEWLY_ESTABLISHED,
    )
    legal_representative = models.ForeignKey('LegalRepresentative', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Legal Representative"))
    issued_date = models.DateField(_("Issued Date"))
    business_type = models.ForeignKey('BusinessType', on_delete=models.CASCADE, verbose_name=_("Business Type"))
    main_industry = models.ForeignKey('Industry', on_delete=models.CASCADE, related_name='+', verbose_name=_("Main Industry"))
    headquarters_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='+', verbose_name=_("Headquarters Address"))
    
    def __str__(self):
        return self.company_name
    

class BusinessStatusChange(models.Model):
    class Meta:
        verbose_name = _("Business Status Change")
        verbose_name_plural = _("Business Status Changes")

    business = models.ForeignKey(Business, on_delete=models.CASCADE)  # Khóa ngoại đến model Business
    old_status = models.CharField(
        _("Old Status"),
        max_length=5,
        choices=BusinessStatus.choices,
    )  # Trạng thái cũ của doanh nghiệp
    new_status = models.CharField(
        _("New Status"),
        max_length=5,
        choices=BusinessStatus.choices,
    )  # Trạng thái mới của doanh nghiệp
    change_date = models.DateField(auto_now_add=True)  # Ngày thay đổi trạng thái
    # changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Người thực hiện thay đổi trạng thái

    def __str__(self):
        return f"{self.business}, {self.old_status}, {self.new_status}, {self.change_date}"
class LegalRepresentative(models.Model):
    class Meta:
        verbose_name = _("Legal Representative")
        verbose_name_plural = _("Legal Representatives")

    name = models.CharField(_("Name"),max_length=255)  # Họ và tên
    gender = models.CharField(_("Gender"),max_length=10)  # Giới tính
    position = models.CharField(_("Position"), max_length=255)  # Chức danh
    dob = models.DateField(_("Date of Birth"))  # Sinh ngày (Date of Birth)
    ethnicity = models.CharField(_("Ethnicity"), max_length=50)  # Dân tộc
    nationality = models.CharField(_("Nationality"), max_length=50)  # Quốc tịch
    id_type = models.CharField(_("ID Type"), max_length=255)  # Loại giấy tờ pháp lý (The can cuoc cong dan)
    id_number = models.CharField(_("ID Number"), max_length=20)  # Số giấy tờ pháp lý
    id_issuance_date = models.DateField(_("ID Issuance Date"))  # Ngày cấp
    id_issuance_place = models.CharField(_("ID Issuance Place"), max_length=255)  # Nơi cấp
    residence_address = models.TextField(_("Residence Address") )  # Địa chỉ thường trú
    contact_address = models.TextField( _("Contact Address"))  # Địa chỉ liên lạc

    def __str__(self):
        return self.name

class Owner(models.Model):
    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")

    name = models.CharField(_("Name"), max_length=255)  # Họ và tên
    gender = models.CharField(_("Gender"), max_length=10)  # Giới tính
    dob = models.DateField(_("Date of Birth"))  # Ngày, tháng, năm sinh
    ethnicity = models.CharField(_("Ethnicity"), max_length=50)  # Dân tộc
    nationality = models.CharField(_("Nationality"), max_length=50)  # Quốc tịch
    id_type = models.CharField(_("ID Type"), max_length=100)  # Loại giấy tờ pháp lý
    id_number = models.CharField(_("ID Number"), max_length=20)  # Số giấy tờ pháp lý
    id_issuance_date = models.DateField(_("ID Issuance Date"))  # Ngày cấp
    id_issuance_place = models.CharField(_("ID Issuance Place"), max_length=255)  # Nơi cấp
    residence_address = models.TextField(_("Residence Address"))  # Địa chỉ thường trú
    contact_address = models.TextField(_("Contact Address"))  # Địa chỉ liên lạc


    def __str__(self):
        return self.name

class BusinessOwner(models.Model):
    class Meta:
        verbose_name = _("Business Owner")
        verbose_name_plural = _("Business Owners")

    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Business"))  # Khóa ngoại đến model Business
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name=_("Owner"))  # Khóa ngoại đến model Owner

    def __str__(self):
        return f"{self.business}, {self.owner}"
class BusinessType(models.Model):
    class Meta:
        verbose_name = _("Business Type")
        verbose_name_plural = _("Business Types")

    type_description = models.CharField(_("Type Description"), max_length=255)  # Mô tả về loại hình doanh nghiệp

    def __str__(self):
        return self.type_description
class BusinessTypeStatus(models.Model):
    class Meta:
        verbose_name = _("Business Type Status")
        verbose_name_plural = _("Business Type Statuses")

    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, verbose_name=_("Business Type"))  # Khóa ngoại đến model BusinessType
    status = models.CharField(
        _("Status"),
        max_length=5,
        choices=BusinessStatus.choices,
    )  # Trạng thái

    def __str__(self):
        return f"{self.business_type}, {self.get_status_display()}"
    
    def get_status_display_full(self):
        return dict(BusinessStatus.choices)[self.status]


class BusinessProcessStep(models.Model):
    class Meta:
        verbose_name = _("Business Process Step")
        verbose_name_plural = _("Business Process Steps")

    business_type_status = models.ForeignKey(BusinessTypeStatus, on_delete=models.CASCADE, verbose_name=_("Business Type Status"))  # Khóa ngoại đến model BusinessTypeStatus
    step_name = models.CharField(_("Step Name"), max_length=255)  # Tên của bước trong quy trình
    step_order = models.IntegerField(_("Step Order"))  # Thứ tự của bước trong quy trình
    step_description = models.TextField(_("Step Description"))  # Mô tả nội dung cho mỗi bước

    def __str__(self):
        return self.step_name
class Industry(models.Model):
    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")

    activity_code = models.IntegerField(_("Activity Code"))  # Mã của ngành nghề kinh doanh
    activity_name = models.CharField(_("Activity Name"), max_length=255)  # Tên của ngành nghề kinh doanh

    def __str__(self):
        return self.activity_name
class BusinessIndustry(models.Model):
    class Meta:
        verbose_name = _("Business Industry")
        verbose_name_plural = _("Business Industries")

    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Business"))  # Khóa ngoại đến model Business
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, verbose_name=_("Industry"))  # Khóa ngoại đến model Industry

    def __str__(self):
        return f"{self.business}, {self.industry}"

class ActivityField(models.Model):
    class Meta:
        verbose_name = _("Activity Field")
        verbose_name_plural = _("Activity Fields")

    field_code = models.IntegerField(_("Field Code"))  # Mã của lĩnh vực hoạt động
    field_name = models.CharField(_("Field Name"), max_length=255)  # Tên của lĩnh vực hoạt động

    def __str__(self):
        return self.field_name
class BusinessActivityField(models.Model):
    class Meta:
        verbose_name = _("Business Activity Field")
        verbose_name_plural = _("Business Activity Fields")

    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Business"))  # Khóa ngoại đến model Business
    activity_field = models.ForeignKey(ActivityField, on_delete=models.CASCADE, verbose_name=_("Activity Field"))  # Khóa ngoại đến model ActivityField

    def __str__(self):
        return f"{self.business}, {self.activity_field}"

class Contacts(models.Model):
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    phone = models.CharField(_("Phone"), max_length=255)  # Số điện thoại
    email = models.CharField(_("Email"), max_length=255)  # Địa chỉ email
    fax = models.CharField(_("Fax"), max_length=255)  # Số fax
    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Business"))  # Khóa ngoại đến model Business

    def __str__(self):
        return f"{self.phone}, {self.email}, {self.fax}"

class Address(models.Model):
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    detail = models.CharField(_("Detail"), max_length=255)  # Địa chỉ chi tiết
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name=_("Province"))
    district = models.ForeignKey('District', on_delete=models.CASCADE, verbose_name=_("District"))
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE, verbose_name=_("Ward"))  # Khóa ngoại đến model Ward

    def __str__(self):
        return f"{self.detail}, {self.ward}, {self.district}, {self.province}"
class BusinessAddress(models.Model):
    class Meta:
        verbose_name = _("Business Address")
        verbose_name_plural = _("Business Addresses")

    business = models.ForeignKey(Business, on_delete=models.CASCADE, verbose_name=_("Business"))  # Khóa ngoại đến model Business
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name=_("Address"))  # Khóa ngoại đến model Address

    def __str__(self):
        return f"{self.business}, {self.address}"
    
class AdministrativeUnit(models.Model):
    class Meta:
        verbose_name = _("Administrative Unit")
        verbose_name_plural = _("Administrative Units")

    full_name = models.CharField(_("Full Name"), max_length=255)
    full_name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    short_name = models.CharField(_("Short Name"), max_length=255, blank=True)
    short_name_en = models.CharField(_("Short Name (English)"), max_length=255, blank=True)
    code_name = models.CharField(_("Code Name"), max_length=255, blank=True)
    code_name_en = models.CharField(_("Code Name (English)"), max_length=255, blank=True)

    def __str__(self):
        return self.name
class AdministrativeRegion(models.Model):
    class Meta:
        verbose_name = _("Administrative Region")
        verbose_name_plural = _("Administrative Regions")

    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(_("Name"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    code_name = models.CharField(_("Code Name"), max_length=255, blank=True)
    code_name_en = models.CharField(_("Code Name (English)"), max_length=255, blank=True)

    def __str__(self):
        return self.name
class Province(models.Model):
    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")

    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(_("Name"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True)
    full_name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    code_name = models.CharField(_("Code Name"), max_length=255, blank=True)
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, verbose_name=_("Administrative Unit"))
    administrative_region = models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE, verbose_name=_("Administrative Region"))

    def __str__(self):
        return self.name
class District(models.Model):
    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(_("Name"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True)
    full_name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    code_name = models.CharField(_("Code Name"), max_length=255, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_("Province"))
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, verbose_name=_("Administrative Unit"))

    def __str__(self):
        return self.name
class Ward(models.Model):
    class Meta:
        verbose_name = _("Ward")
        verbose_name_plural = _("Wards")

    code = models.BigIntegerField(primary_key=True)
    name = models.CharField(_("Name"), max_length=255)
    name_en = models.CharField(_("Name (English)"), max_length=255, blank=True)
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True)
    full_name_en = models.CharField(_("Full Name (English)"), max_length=255, blank=True)
    code_name = models.CharField(_("Code Name"), max_length=255, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_("District"))
    administrative_unit = models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE, verbose_name=_("Administrative Unit"))

    def __str__(self):
        return self.name
