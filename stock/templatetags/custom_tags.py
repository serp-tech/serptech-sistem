from django import template
from stock.utils import format_currency


register = template.Library()


@register.filter(name='is_date_field')
def is_date_field(field):
    return getattr(field.field.widget, 'input_type', None) == 'date'

@register.filter
def format_currency_filter(value):
    return format_currency(value)

