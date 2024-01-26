from django.contrib import admin
from .models import Business, LegalRepresentative, Owner, BusinessOwner, BusinessType, Industry, BusinessIndustry, ActivityField, BusinessActivityField, Contacts, Addresses, AdministrativeUnit, Province, District, Ward, AdministrativeRegion
from .models_admin import BusinessAdmin, LegalRepresentativeAdmin, OwnerAdmin, BusinessOwnerAdmin, BusinessTypeAdmin, IndustryAdmin, BusinessIndustryAdmin, ActivityFieldAdmin, BusinessActivityFieldAdmin, ContactsAdmin, AddressesAdmin, AdministrativeUnitAdmin, ProvinceAdmin, DistrictAdmin, WardAdmin, AdministrativeRegionAdmin
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
admin.site.register(Addresses, AddressesAdmin)
admin.site.register(AdministrativeUnit, AdministrativeUnitAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(AdministrativeRegion, AdministrativeRegionAdmin)

admin.site.index_title =  "Business Registration Administration"

