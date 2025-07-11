# encoding: utf-8

'''📜 Dicominator tags: custom template filters for DICOM data.'''

from django import template

register = template.Library()


@register.filter
def hex_format(value):
    '''Convert an integer to hexadecimal format without the 0x prefix.'''
    if value is None:
        return ''
    try:
        return f'{int(value):04x}'
    except (ValueError, TypeError):
        return str(value) 