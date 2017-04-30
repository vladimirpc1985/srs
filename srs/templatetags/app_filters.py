from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(d, key):
    a = int(key)
    a = a-1
    return d[a]

@register.filter(name='lookup_pk')
def lookup_pk(d, key):
    a = int(key)
    a = a-1
    return d[a].pk

@register.filter(name='lookup_label')
def lookup_label(d, key):
    a = int(key)
    a = a-1
    return d[a].label
