from django import template

register = template.Library()

@register.filter
def strip_start(value):
    if isinstance(value, str):
        return value.lstrip()
    return value