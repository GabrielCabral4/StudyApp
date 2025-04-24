from django import template

register = template.Library()

@register.filter
def get_nome_mes(mes_numero):
    meses = [
        "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return meses[int(mes_numero)]