from django import template
from stock.utils import format_currency


register = template.Library()


@register.filter(name='is_date_field')
def is_date_field(field):
    return getattr(field.field.widget, 'input_type', None) == 'date'


@register.filter
def get_transacao_tipo(transacao):
    if hasattr(transacao, 'data_vencimento'):
        return 'Conta a Pagar'
    elif hasattr(transacao, 'data_recebimento'):
        return 'Conta a Receber'
    return 'Desconhecido'


@register.filter
def format_currency_filter(value):
    return format_currency(value)