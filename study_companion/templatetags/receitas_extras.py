from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(value, search_term):
    """
    Destaca as ocorrências do termo de pesquisa no texto.
    """
    if not search_term or not value:
        return value
    
    try:
        escaped_term = re.escape(search_term)
        
        # Substitui o termo por uma versão destacada
        pattern = re.compile(f'({escaped_term})', re.IGNORECASE)
        highlighted = pattern.sub(r'<mark class="highlight">\1</mark>', str(value))
        
        return mark_safe(highlighted)
    except:
        return value