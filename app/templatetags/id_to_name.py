from django.template import Library
from pythonAPI.dwapi import datawiz

register = Library()
dw = datawiz.DW()

@register.simple_tag
def id2name(id):
    return  dw.id2name([id], 'product').get(id)