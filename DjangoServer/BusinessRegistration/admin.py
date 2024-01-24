from django.contrib import admin
from .models import Companies, MainBusinessActivities, BusinessActivities, Addresses, Contacts, BusinessTypes

# admin.site.site_header =  "Business Registration Administration"
# admin.site.site_title =  "Business Registration Administration"
admin.site.index_title =  "Business Registration Administration"

admin.site.register(Companies)
admin.site.register(MainBusinessActivities)
admin.site.register(BusinessActivities)
admin.site.register(Addresses)
admin.site.register(Contacts)
admin.site.register(BusinessTypes)
