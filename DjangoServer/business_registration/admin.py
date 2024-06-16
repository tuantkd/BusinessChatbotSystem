from django.contrib import admin
from .models import Address, Business, BusinessProcessStep, BusinessTypeStatus, LegalRepresentative, Owner, BusinessOwner, BusinessType, Industry, BusinessIndustry, ActivityField, BusinessActivityField, Contacts, AdministrativeUnit, Province, District, Ward, AdministrativeRegion
from .models_admin import AddressAdmin, BusinessAdmin, BusinessProcessStepAdmin, BusinessTypeStatusAdmin, LegalRepresentativeAdmin, OwnerAdmin, BusinessOwnerAdmin, BusinessTypeAdmin, IndustryAdmin, BusinessIndustryAdmin, ActivityFieldAdmin, BusinessActivityFieldAdmin, ContactsAdmin, AddressesAdmin, AdministrativeUnitAdmin, ProvinceAdmin, DistrictAdmin, WardAdmin, AdministrativeRegionAdmin
from django.contrib.auth.models import User, Group, Permission

if admin.site.is_registered(User):
    admin.site.unregister(User)
if admin.site.is_registered(Group):
    admin.site.unregister(Group)
if admin.site.is_registered(Permission):
    admin.site.unregister(Permission)

admin.site.register(Address, AddressAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(LegalRepresentative, LegalRepresentativeAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(BusinessOwner, BusinessOwnerAdmin)
admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(BusinessIndustry, BusinessIndustryAdmin)
admin.site.register(ActivityField, ActivityFieldAdmin)
admin.site.register(BusinessActivityField, BusinessActivityFieldAdmin)
admin.site.register(Contacts, ContactsAdmin)

# admin.site.register(AdministrativeUnit, AdministrativeUnitAdmin)
# admin.site.register(Province, ProvinceAdmin)
# admin.site.register(District, DistrictAdmin)
# admin.site.register(Ward, WardAdmin)
# admin.site.register(AdministrativeRegion, AdministrativeRegionAdmin)
admin.site.register(BusinessTypeStatus, BusinessTypeStatusAdmin)
admin.site.register(BusinessProcessStep, BusinessProcessStepAdmin)

admin.site.index_title =  "Business Registration Administration"


