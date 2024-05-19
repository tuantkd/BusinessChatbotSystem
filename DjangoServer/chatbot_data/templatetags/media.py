from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='media')
def media(value):
    return f'{settings.MEDIA_URL}{value}'
