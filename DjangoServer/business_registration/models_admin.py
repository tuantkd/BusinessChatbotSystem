from django.contrib import admin
from django.utils.html import format_html
from .models import Contacts

# class AddressInline(admin.TabularInline):
#     model = Addresses
#     extra = 1  # how many rows to show

#     class Media:
#         js = ('js/address.js',)  # path to your JavaScript file
        
class ContactInline(admin.TabularInline):
    model = Contacts
    extra = 1  # how many rows to show

class AddressAdmin(admin.ModelAdmin):
    list_display = ('detail', 'ward', 'district', 'province')
    list_display_links = ('detail',)
    search_fields = ('detail', 'ward__name', 'district__name', 'province__name')
    list_per_page = 25

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_code', 'company_name', 'detail', 'capital', 'status', 'legal_representative', 'issued_date', 'business_type', 'main_industry', 'headquarters_address_with_buttons')

    def headquarters_address_with_buttons(self, obj):
        if obj.headquarters_address:
            edit_url = f"/admin/your_app_name/address/{obj.headquarters_address.id}/change/"
            view_url = f"/admin/your_app_name/address/{obj.headquarters_address.id}/"
            add_url = "/admin/your_app_name/address/add/"
            return format_html(
                '<a class="button" href="{}">Edit</a>&nbsp;<a class="button" href="{}">View</a>&nbsp;<a class="button" href="{}">Add</a>',
                edit_url, view_url, add_url
            )
        else:
            add_url = "/admin/your_app_name/address/add/"
            return format_html('<a class="button" href="{}">Add</a>', add_url)

    headquarters_address_with_buttons.short_description = 'Headquarters Address'

class LegalRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    list_display_links = ('name', 'position')
    #list_filter = ('name', 'position')
    search_fields = ('name', 'position')
    list_per_page = 25

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    #list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 25

class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ('business', 'owner')
    list_display_links = ('business', 'owner')
    #list_filter = ('business', 'owner')
    search_fields = ('business', 'owner')

class BusinessTypeAdmin(admin.ModelAdmin):
    list_display = ('type_description',)
    list_display_links = ('type_description',)
    #list_filter = ('type_description',)
    search_fields = ('type_description',)
    list_per_page = 25

class IndustryAdmin(admin.ModelAdmin):
    list_display = ('activity_code', 'activity_name')
    list_display_links = ('activity_code', 'activity_name')
    # list_filter = ('activity_code', 'activity_name')
    search_fields = ('activity_code', 'activity_name')
    list_per_page = 25

class BusinessIndustryAdmin(admin.ModelAdmin):
    list_display = ('business', 'industry')
    list_display_links = ('business', 'industry')
    #list_filter = ('business', 'industry')
    search_fields = ('business', 'industry')
    list_per_page = 25

class ActivityFieldAdmin(admin.ModelAdmin):
    list_display = ('field_code', 'field_name')
    list_display_links = ('field_code', 'field_name')
    #list_filter = ('field_code', 'field_name')
    search_fields = ('field_code', 'field_name')
    list_per_page = 25

class BusinessActivityFieldAdmin(admin.ModelAdmin):
    list_display = ('business', 'activity_field')
    list_display_links = ('business', 'activity_field')
    #list_filter = ('business', 'activity_field')
    search_fields = ('business', 'activity_field')
    list_per_page = 25

class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'fax', 'business')
    list_display_links = ('phone', 'email', 'fax', 'business')
    #list_filter = ('phone', 'email', 'fax', 'business')
    search_fields = ('phone', 'email', 'fax', 'business')
    list_per_page = 25

class AddressesAdmin(admin.ModelAdmin):
    list_display = ('detail', 'ward', 'business')
    list_display_links = ('detail', 'ward', 'business')
    #list_filter = ('detail', 'ward', 'business')
    search_fields = ('detail', 'ward', 'business')
    list_per_page = 25

class AdministrativeUnitAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')
    list_display_links = ('full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')
    #list_filter = ('full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')
    search_fields = ('full_name', 'full_name_en', 'short_name', 'short_name_en', 'code_name', 'code_name_en')
    list_per_page = 25

class AdministrativeRegionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'name_en', 'code_name_en')
    list_display_links = ('code', 'name', 'name_en', 'code_name_en')
    #list_filter = ('code', 'name', 'name_en', 'code_name_en')
    search_fields = ('code', 'name', 'name_en', 'code_name_en')
    list_per_page = 25


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'administrative_unit', 'administrative_region')
    list_display_links = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'administrative_unit', 'administrative_region')
    #list_filter = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'administrative_unit', 'administrative_region')
    search_fields = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'administrative_unit', 'administrative_region')
    list_per_page = 25
    readonly_fields = ('administrative_unit', 'administrative_region',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'province', 'administrative_unit')
    list_display_links = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'province', 'administrative_unit')
    #list_filter = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'province', 'administrative_unit')
    search_fields = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'province', 'administrative_unit')
    list_per_page = 25
    readonly_fields = ('administrative_unit','province')

class WardAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'district', 'administrative_unit')
    list_display_links = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'district', 'administrative_unit')
    #list_filter = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'district', 'administrative_unit')
    search_fields = ('code', 'name', 'name_en', 'full_name', 'full_name_en', 'code_name', 'district', 'administrative_unit')
    list_per_page = 25
    readonly_fields = ('administrative_unit','district')


class BusinessTypeStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'business_type')
    list_display_links = ('status', 'business_type')
    list_filter = ('status', 'business_type')
    search_fields = ('status', 'business_type')
    list_per_page = 25
    

class BusinessProcessStepAdmin(admin.ModelAdmin):
    list_display = ('business_type_status', 'step_name', 'step_order', 'step_description')
    list_display_links = ('business_type_status', 'step_name', 'step_order', 'step_description')
    list_filter = ('business_type_status',)
    search_fields = ('business_type_status', 'step_name', 'step_order', 'step_description')
    list_per_page = 25

