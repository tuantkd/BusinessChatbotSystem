import datetime
import json
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def chatDate(value):
    if not value:
        # Value is empty or None, return an empty string
        return ''
    # Convert the timestamp to a datetime object
    timestamp = datetime.datetime.fromtimestamp(float(value))
    # Format the datetime object as a string
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

@register.filter
def as_json(data):
    return json.dumps(data, indent=4)

@register.filter
def length_filtered(queryset, expression_id):
    return len([obj for obj in queryset if obj.expression.id == expression_id])