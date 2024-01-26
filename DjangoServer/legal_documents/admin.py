from django.contrib import admin
from django.contrib import admin
from .models import Laws, Decrees, Circulars, Decisions

admin.site.index_title =  "Legal Documents Administration"
admin.site.register(Laws)
admin.site.register(Decrees)
admin.site.register(Circulars)
admin.site.register(Decisions)
