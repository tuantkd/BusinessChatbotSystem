from django.contrib import admin
from .models import Intents, Entities, Actions, Stories, Rules, Responses, History
admin.site.index_title =  "Chatbot Data Administration"
admin.site.register(Intents)
admin.site.register(Entities)
admin.site.register(Actions)
admin.site.register(Stories)
admin.site.register(Rules)
admin.site.register(Responses)
admin.site.register(History)
