from django import template

register = template.Library()

@register.filter
def dias_ativos(dias_str, nomes_dias):
    nomes = nomes_dias.split(",")
    dias_str = dias_str.ljust(7, "0") 
    return ", ".join([nomes[i] for i in range(7) if dias_str[i] == "1"])