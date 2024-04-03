from django.contrib import admin
from .models import Laws, Decrees, Circulars, Decisions

admin.site.index_title =  "Legal Documents Administration"

class LawsAdmin(admin.ModelAdmin):
    list_display = ('law_number', 'law_name', 'law_link')
    list_display_links = ('law_number', 'law_name')
    list_filter = ('law_number', 'law_name')
    search_fields = ('law_number', 'law_name', 'law_link')
    list_per_page = 25

class DecreesAdmin(admin.ModelAdmin):
    list_display = ('decree_number', 'decree_name', 'decree_link')
    list_display_links = ('decree_number', 'decree_name')
    list_filter = ('decree_number', 'decree_name')
    search_fields = ('decree_number', 'decree_name', 'decree_link')
    list_per_page = 25

class CircularsAdmin(admin.ModelAdmin):
    list_display = ('circular_number', 'circular_name', 'circular_link')
    list_display_links = ('circular_number', 'circular_name')
    list_filter = ('circular_number', 'circular_name')
    search_fields = ('circular_number', 'circular_name', 'circular_link')
    list_per_page = 25

class DecisionsAdmin(admin.ModelAdmin):
    list_display = ('decision_number', 'decision_name', 'decision_link')
    list_display_links = ('decision_number', 'decision_name')
    list_filter = ('decision_number', 'decision_name')
    search_fields = ('decision_number', 'decision_name', 'decision_link')
    list_per_page = 25

admin.site.register(Laws, LawsAdmin)
admin.site.register(Decrees, DecreesAdmin)
admin.site.register(Circulars, CircularsAdmin)
admin.site.register(Decisions, DecisionsAdmin)
