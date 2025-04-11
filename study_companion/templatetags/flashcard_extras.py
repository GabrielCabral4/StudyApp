from django import template

register = template.Library()

@register.filter
def get_dificuldade_class(value):
    if value == 1:
        return "easy"
    elif value == 2:
        return "medium"
    elif value == 3:
        return "hard"
    return "easy"