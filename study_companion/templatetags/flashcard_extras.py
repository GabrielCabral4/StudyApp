from django import template

register = template.Library()

@register.filter
def get_dificuldade_class(dificuldade):
    """Converte valor numérico ou texto para classe CSS"""
    if isinstance(dificuldade, str) and dificuldade.isdigit():
        dificuldade = int(dificuldade)
    
    class_map = {
        1: 'facil',
        2: 'medio',
        3: 'dificil',
        '1': 'facil',
        '2': 'medio',
        '3': 'dificil',
        'FACIL': 'facil',
        'MEDIO': 'medio',
        'DIFICIL': 'dificil'
    }
    return class_map.get(dificuldade, '')

@register.filter
def get_dificuldade_value(dificuldade):
    """Converte a dificuldade para valor numérico"""
    dificuldades = {
        'FACIL': '1',
        'MEDIO': '2',
        'DIFICIL': '3'
    }
    return dificuldades.get(dificuldade, '1')